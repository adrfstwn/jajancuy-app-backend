package service

import (
	"errors"
	"toko_services/internal/domain"
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
func (s *TokoService) CreateToko(toko domain.Toko) (int, error) {
	if toko.Name == "" {
		return 0, errors.New("name is required")
	}
	if toko.Description == "" {
		return 0, errors.New("description is required")
	}
	if toko.OwnerID == 0 {
		return 0, errors.New("owner ID is required")
	}

	return s.repo.CreateToko(toko)
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
