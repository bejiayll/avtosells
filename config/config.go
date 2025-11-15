package config

import (
	"log"
	"os"
	"time"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env               string `yaml:"env" env-defaul:"development"`
	DatabaseURL       string `yaml:"db_url" env-required:"true"`
	DatabasePasswowrd string `yaml:"db_password" env-required:"true"`
	HTTPServer        `yaml:"http_server"`
}

type HTTPServer struct {
	Port        string        `yaml:"port" env-default:":8080"`
	Timeout     time.Duration `yaml:"timeout" env-default:"5s"`
	IdleTimeout time.Duration `yaml:"idle_timeout" env-default:"30s"`
}

func MustLoad() *Config {

	configPath := "./config/config.yaml"

	if _, err := os.Stat(configPath); err != nil {
		log.Fatalf("❌ Error when opening config file %s: ", &err)
	}
	log.Println("✅ Config file is exists")

	var cfg Config

	err := cleanenv.ReadConfig(configPath, &cfg)
	if err != nil {
		log.Fatalf("❌ Error when reading config %s", err)
	}
	log.Println("✅ Config loaded")

	return &cfg
}
