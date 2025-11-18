package config

type User struct {
	ID           uint16 `json:"id"`
	Name         string `json:"name"`
	Family_name  string `json:"family_name"`
	Email        string `json:"email"`
	Phone_number string `json:"phone_number"`
	Password     string `json:"password"`
	Role         string `json:"role"`
}

type Field struct {
	Field string `json:"field"`
	Tank  string `json:"tank"`
}
