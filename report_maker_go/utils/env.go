package utils

import (
	"fmt"
	"log"
	"os"
)

func GetRequiredEnv(envName string) string {
	value, isExists := os.LookupEnv(envName)
	if !isExists {
		log.Fatal(
			fmt.Sprintf("Environment variable '%s' was not provided", envName),
		)
		os.Exit(1)
	}

	return value
}
