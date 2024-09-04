package handlers

import (
	"encoding/json"
	"html/template"
	"log"
	"net/http"
	"report_maker_go/utils"
)

func GetReport(response http.ResponseWriter, request *http.Request) {
	reportData := make(map[string]map[string]int)

	for ip, keysPair := range utils.GlobalConfig.HOSTS_KEY_PARES {
		sshClient := utils.ConnectToHost(ip, keysPair.PrivateKey)

		if sshClient == nil {
			log.Printf("Failed to connect to %v", ip)
			continue
		}

		utils.ExecuteCommand(sshClient, "bash generate_raw_report.sh")

		commandOutput, err := utils.ExecuteCommand(sshClient, "cat raw_report.json")
		if err != nil {
			log.Printf("Error fetching report from %v: %v", ip, err)
			continue
		}

		log.Printf("Received raw report from %v => %v", ip, commandOutput)

		var parsedReport map[string]int
		if err := json.Unmarshal([]byte(commandOutput), &parsedReport); err != nil {
			log.Printf("Error parsing JSON report from %v: %v", ip, err)
			continue
		}

		reportData[ip] = parsedReport
	}

	tmpl, err := template.ParseFiles("templates/index.html")
	if err != nil {
		http.Error(response, err.Error(), http.StatusInternalServerError)
		log.Print(err)
		return
	}

	err = tmpl.Execute(response, map[string]interface{}{
		"report_data": reportData,
	})
	if err != nil {
		http.Error(response, err.Error(), http.StatusInternalServerError)
		log.Print(err)
	}
}
