package main

import (
	"log"

	"github.com/bejiayll/avtosells.git/config"
	"github.com/bejiayll/avtosells.git/router"
)

func main() {
	cfg := config.MustLoad()
	log.Printf("Server port: %s", cfg.Port)
	router.RunServer(cfg.Port)
}
