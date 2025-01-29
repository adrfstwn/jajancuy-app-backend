package service

import (
	"errors"
	"fmt"
	"strconv"
	"toko_services/internal/domain"
	"toko_services/pkg/logger"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)

// TokoService is the implementation of the TokoService interface
type TokoService struct {
	repo domain.TokoDomain
}

// NewTokoService creates a new instance of TokoService
func NewTokoService(repo domain.TokoDomain) *TokoService {
	return &TokoService{repo: repo}
}

// CreateToko adds a new toko (store) to the database
func (s *TokoService) CreateToko(toko domain.Toko, c *gin.Context) (int, error) {

	log := logger.New()

	// Ambil klaim dari context
	claims, exists := c.Get("claims")
	if !exists {
		log.Error("please log in instead")
		return 0, errors.New("please log in instead")
	}

	// Ambil user_id dari klaim, pastikan klaim bertipe jwt.MapClaims
	claimsMap, ok := claims.(jwt.MapClaims)
	if !ok {
		log.Error("Invalid claims format")
		return 0, errors.New("invalid token claims format")
	}

	// Debugging: Menampilkan klaim untuk memastikan isinya
	log.Info(fmt.Sprintf("Token claims: %v", claimsMap))

	// Ambil user_id dari klaim dengan pengecekan terhadap tipe data
	userID, ok := claimsMap["user_id"].(float64)
	if !ok {
		log.Info("user_id type assertion failed, checking other types")
		// Coba cast ke tipe string atau tipe lainnya
		if userIDStr, ok := claimsMap["user_id"].(string); ok {
			log.Info(fmt.Sprintf("user_id found as string: %s", userIDStr))
			// Coba konversi string ke int jika perlu
			userIDInt, err := strconv.Atoi(userIDStr)
			if err != nil {
				log.Error("Error converting user_id from string to int")
				return 0, errors.New("invalid user ID format")
			}
			userID = float64(userIDInt) // Ubah menjadi float64 setelah konversi
		} else {
			log.Error("User ID not found in token claims")
			return 0, errors.New("user ID not found in token claims")
		}
	}

	// Verifikasi nilai userID sebelum diteruskan
	log.Info(fmt.Sprintf("User ID extracted: %v", userID))

	// Konversi userID ke int secara eksplisit
	userIDInt := int(userID)

	// Menetapkan OwnerID toko dengan user_id dari klaim
	toko.OwnerID = userIDInt

	// Validasi data toko
	if toko.Name == "" {
		log.Error("name is required")
		return 0, errors.New("name is required")
	}
	if toko.Description == "" {
		log.Error("description is required")
		return 0, errors.New("description is required")
	}
	if toko.Address == "" {
		log.Error("address is required")
		return 0, errors.New("address is required")
	}

	// Panggil repo untuk menyimpan toko
	tokoID, err := s.repo.CreateToko(toko)
	if err != nil {
		log.Error("Failed to create toko: " + err.Error())
		return 0, err
	}

	log.Info("Toko created successfully with ID: " + strconv.Itoa(tokoID))
	return tokoID, nil
}

// GetTokoByID retrieves a toko by its ID
func (s *TokoService) GetTokoByID(id int) (*domain.Toko, error) {
	if id <= 0 {
		return nil, errors.New("invalid ID")
	}
	return s.repo.GetTokoByID(id)
}

// GetAllToko retrieves all toko records
func (s *TokoService) GetAllToko() ([]domain.Toko, error) {
	return s.repo.GetAllToko()
}

// UpdateToko updates the details of an existing toko
func (s *TokoService) UpdateToko(toko domain.Toko) error {
	if toko.ID <= 0 {
		return errors.New("invalid ID")
	}
	if toko.Name == "" {
		return errors.New("name is required")
	}
	if toko.Description == "" {
		return errors.New("description is required")
	}
	if toko.Address == "" {
		return errors.New("address is required")
	}
	if toko.OwnerID == 0 {
		return errors.New("owner ID is required")
	}

	return s.repo.UpdateToko(toko)
}

// DeleteToko removes a toko by its ID
func (s *TokoService) DeleteToko(id int) error {
	if id <= 0 {
		return errors.New("invalid ID")
	}
	return s.repo.DeleteToko(id)
}
