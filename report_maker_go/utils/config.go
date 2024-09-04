package utils

type globalConfig struct {
	HOSTS_KEY_PARES map[string]*ResponseRemoteHostKeyPair
}

var GlobalConfig globalConfig = globalConfig{}
