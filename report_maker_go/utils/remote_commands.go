package utils

import (
	"bytes"
	"log"
	"net"

	"golang.org/x/crypto/ssh"
)

func ConnectToHost(ip, privateKey string) *ssh.Client {
	privateKeySigner, _ := ssh.ParsePrivateKey([]byte(privateKey))
	sshConfig := &ssh.ClientConfig{
		User: "admin",
		Auth: []ssh.AuthMethod{
			ssh.PublicKeys(privateKeySigner),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	client, err := ssh.Dial(
		"tcp",
		net.JoinHostPort(ip, "22"),
		sshConfig,
	)
	if err != nil {
		log.Print("Error connecting SSH:", err)
		return nil
	}
	return client
}

func CloseSSHConn(sshClient *ssh.Client) {
	sshClient.Close()
}

func ExecuteCommand(sshClient *ssh.Client, command string) (string, error) {
	session, err := sshClient.NewSession()
	if err != nil {
		log.Printf("Failed to establish session: %v", err)
		return "", err
	}

	defer session.Close()
	var buffOut bytes.Buffer
	session.Stdout = &buffOut

	var buffErr bytes.Buffer
	session.Stderr = &buffErr

	err = session.Run(command)
	if err != nil {
		log.Printf("Command execution failed: %v (%v)", err, buffErr.String())
		return "", err
	}
	return buffOut.String(), err
}
