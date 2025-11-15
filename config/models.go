package config

type User struct {
	id           uint16 `json:"id"`
	name         string `json:"name"`
	family_name  string `json:"family_name"`
	father_name  string `json:"father_name"`
	email        string `json:"email"`
	phone_number string `json:"phone_number"`
}

type Field struct {
	Field string `json:"field"`
}
