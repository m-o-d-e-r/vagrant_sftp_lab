package main

import (
	"errors"
	"fmt"
	"log"
	"net/http"
	"report_maker_go/handlers"
	"report_maker_go/utils"
)

func main() {
	CERT_PROVIDER_HOST := utils.GetRequiredEnv("CERT_PROVIDER_HOST")
	CERT_PROVIDER_PORT := utils.GetRequiredEnv("CERT_PROVIDER_PORT")

	var remoteHostsIPS []string = utils.GetRemoteHostsIPs(
		CERT_PROVIDER_HOST,
		CERT_PROVIDER_PORT,
	)

	log.Print(fmt.Sprintf("Raw reports should be gathered from: %v", remoteHostsIPS))

	utils.GlobalConfig.HOSTS_KEY_PARES = utils.ReceiveAllKeys(
		CERT_PROVIDER_HOST,
		CERT_PROVIDER_PORT,
		remoteHostsIPS,
	)

	http.HandleFunc("/", handlers.GetReport)

	log.Print("Server started...")
	err := http.ListenAndServe(":8080", nil)

	if errors.Is(err, http.ErrServerClosed) {
		log.Fatal("server closed\n")
	} else if err != nil {
		log.Fatal("error starting server: %s\n", err)
	}
}
