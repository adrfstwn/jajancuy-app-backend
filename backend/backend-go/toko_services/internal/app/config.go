package app

import (
	"toko_services/pkg/logger"

	"github.com/joho/godotenv"
)

func LoadEnv() {

	err := godotenv.Load()

	log := logger.New()

	if err != nil {
		log.Error("Error loading configuration .env file" + err.Error())
	}

}
