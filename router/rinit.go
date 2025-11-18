package router

import (
	"github.com/bejiayll/avtosells.git/jwt"
	"github.com/gin-gonic/gin"
)

func RunServer(p string) {
	r := gin.Default()

	r.GET("/", Index)
	r.GET("/ping", Ping)

	r.POST("/user", User)
	//r.POST("/test", TestFields)
	// authorized := r.Group("/admin", gin.BasicAuth(gin.Accounts{
	// 	"admin": "password123",
	// 	"user":  "password456",
	// }))

	// authorized.GET("/data", func(c *gin.Context) {
	// 	user := c.MustGet(gin.AuthUserKey).(string)
	// 	c.JSON(200, gin.H{
	// 		"message": "Hello " + user,
	// 		"secret":  "This is protected data",
	// 	})
	// })

	r.POST("/auth/login", loginHandler)

	// auth routes
	auth := r.Group("/api")

	auth.Use(jwt.JWTAuthMiddleware())

	auth.GET("/me", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"user": c.GetString("user"),
			"role": c.GetString("role"),
		})
	})

	auth.GET("/admin/stats", jwt.RequireRole("admin"), func(c *gin.Context) {
		c.JSON(200, gin.H{"stats": "secret"})
	})

	auth.GET("/profile", jwt.RequireRole("admin", "user"), func(c *gin.Context) {
		c.JSON(200, gin.H{"profile": "ok"})
	})

	r.Run(p)
}
