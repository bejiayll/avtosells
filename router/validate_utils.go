package router

import "regexp"

func CheckName(text string) bool {

	invalidChars := regexp.MustCompile(`[\s~!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?0-9]`)
	return invalidChars.MatchString(text)

}
