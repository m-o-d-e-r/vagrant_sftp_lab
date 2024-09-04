package utils

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type ResponseServersIPs struct {
	AllIPs []string `json:"all_ips"`
}

type RequestRemoteHostKeyPair struct {
	IP string `json:"ip"`
}

type ResponseRemoteHostKeyPair struct {
	PrivateKey string `json:"private_key"`
	PublicKey  string `json:"public_key"`
}

func GetRemoteHostsIPs(host, port string) []string {
	response, err := http.Get(
		fmt.Sprintf("http://%s:%s/all_ips", host, port),
	)
	if err != nil {
		log.Fatal("Can not receive all IPs")
	}

	defer response.Body.Close()

	data, _ := io.ReadAll(response.Body)
	var serversIPs ResponseServersIPs
	err = json.Unmarshal(data, &serversIPs)
	if err != nil {
		log.Fatal("Error unmarshalling JSON: ", err)
	}

	return serversIPs.AllIPs
}

func ReceiveKeysByIP(host, port, ip string) *ResponseRemoteHostKeyPair {
	requestPayload, err := json.Marshal(
		RequestRemoteHostKeyPair{IP: ip},
	)

	response, err := http.Post(
		fmt.Sprintf("http://%s:%s/certs", host, port),
		"application/json",
		bytes.NewBuffer(requestPayload),
	)
	if err != nil {
		log.Printf("Can not receive private key for '%s'", ip)
	}

	defer response.Body.Close()

	data, _ := io.ReadAll(response.Body)
	var keysPairResponse ResponseRemoteHostKeyPair
	err = json.Unmarshal(data, &keysPairResponse)
	if err != nil {
		log.Print("Error unmarshalling JSON: ", err)
		return nil
	}
	return &keysPairResponse
}

func ReceiveAllKeys(host, port string, hostsToVisit []string) map[string]*ResponseRemoteHostKeyPair {
	remoteHostsPrivateKeys := make(
		map[string]*ResponseRemoteHostKeyPair,
		len(hostsToVisit),
	)

	var tmpHostPairKeys *ResponseRemoteHostKeyPair
	for _, hostItem := range hostsToVisit {
		tmpHostPairKeys = ReceiveKeysByIP(host, port, hostItem)

		if tmpHostPairKeys == nil {
			continue
		}

		remoteHostsPrivateKeys[hostItem] = ReceiveKeysByIP(host, port, hostItem)
	}

	return remoteHostsPrivateKeys
}
