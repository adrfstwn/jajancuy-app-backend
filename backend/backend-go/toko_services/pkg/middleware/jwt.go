package middleware

import (
	"fmt"
	"net/http"
	"os"
	"strings"

	"toko_services/internal/app"
	"toko_services/pkg/logger"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

func InitSecretKey() []byte {

	// Load .env
	app.LoadEnv()

	// Ambil SECRET_JWT_KEY dari environment
	secretKey := os.Getenv("SECRET_JWT_KEY")
	// if secretKey == "" {
	// 	log.Println("SECRET_JWT_KEY tidak ditemukan! Pastikan environment variable diatur dengan benar.")
	// } else {
	// 	log.Printf("SECRET_JWT_KEY ditemukan: %s\n", secretKey)
	// }
	return []byte(secretKey)
}

// JwtMiddleware: Middleware untuk validasi JWT
func JwtMiddleware() gin.HandlerFunc {

	log := logger.New()

	// Inisialisasi SECRET_JWT_KEY
	SecretKey := InitSecretKey()

	return func(c *gin.Context) {
		// Ambil header Authorization
		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			log.Error("Authorization header is required")
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header is required"})
			c.Abort()
			return
		}

		// Pisahkan format "Bearer <token>"
		tokenString := strings.Split(authHeader, " ")
		if len(tokenString) != 2 {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid authorization format"})
			c.Abort()
			return
		}

		// Verifikasi token JWT
		token, err := jwt.Parse(tokenString[1], func(token *jwt.Token) (interface{}, error) {
			// Periksa apakah algoritma menggunakan HS256
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return SecretKey, nil
		})

		// Periksa hasil parsing token
		if err != nil {
			log.Info("JWT Parse error: " + err.Error())
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token signature"})
			c.Abort()
			return
		}

		// Simpan klaim ke dalam konteks
		if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
			log.Info(fmt.Sprintf("Token valid. Claims: %v", claims))
			c.Set("claims", claims)
			c.Next()
		} else {
			log.Info("Token invalid")
			c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
			c.Abort()
		}
	}
}
