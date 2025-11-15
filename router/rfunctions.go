package router

import (
	"net/http"
	"regexp"

	"github.com/bejiayll/avtosells.git/config"
	"github.com/gin-gonic/gin"
)

func Index(c *gin.Context) {
	c.String(http.StatusOK, "Hi gin!")
}
func Ping(c *gin.Context) {
	c.String(http.StatusOK, "Pong!")
}
func User(c *gin.Context) {
	var user config.User
	if err := c.ShouldBindJSON(&user); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"message": "User received",
		"user":    user,
	})
}

func TestFields(c *gin.Context) {
	var field config.Field
	if err := c.ShouldBindJSON(&field); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	invalidChars := regexp.MustCompile(`[\s~!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]`)
	if invalidChars.MatchString(field.Field) {
		c.JSON(http.StatusBadRequest, gin.H{
			"error":   "INVALID_CHARACTERS",
			"message": "Field allow only letters and numbers",
		})
		return
	}
}
