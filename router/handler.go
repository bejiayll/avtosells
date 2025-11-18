package router

import (
	"log"
	"net/http"
	"time"

	"github.com/bejiayll/avtosells.git/config"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

var users = map[string]config.User{
	"admin@avtosells.org": {
		ID:           0,
		Name:         "Админ",
		Family_name:  "Админов",
		Email:        "admin@avtosells.org",
		Phone_number: "+79998887766",
		Password:     "$2a$10$bRbwR/FJ1ssu4k9cY6VN3.Gfga6lthxgtDTTxkQ0wMIzAb7UVstcS",
		Role:         "admin",
	},
	"ivan2002@mail.ru": {
		ID:           0,
		Name:         "Иван",
		Family_name:  "Иванов",
		Email:        "ivan2002@mail.ru",
		Phone_number: "+78887776655",
		Password:     "$2a$10$bRbwR/FJ1ssu4k9cY6VN3.Gfga6lthxgtDTTxkQ0wMIzAb7UVstcS",
		Role:         "user",
	},
}

type AuthRequest struct {
	Email    string `json:"email" binding:"required"`
	Password string `json:"password" binding:"required"`
}

func loginHandler(c *gin.Context) {
	var req AuthRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid payload"})
		return
	}

	user, ok := users[req.Email]
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "wrong credentials"})
		log.Printf("Email invalid")
		return
	}

	err := bcrypt.CompareHashAndPassword(
		[]byte(user.Password),
		[]byte(req.Password),
	)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "wrong credentials"})
		log.Println("Password invalid")
		return
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub":  req.Email,
		"role": user.Role,
		"exp":  time.Now().Add(time.Hour * 72).Unix(),
	})

	tokenString, err := token.SignedString([]byte(config.MustLoad().JwtSecret))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot create token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"token": tokenString,
	})
}
