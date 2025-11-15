package router

import (
	"github.com/gin-gonic/gin"
)

func RunServer(p string) {
	r := gin.Default()

	r.GET("/", Index)
	r.GET("/ping", Ping)

	r.POST("/user", User)

	r.POST("/test", TestFields)

	r.Run(p)
}
