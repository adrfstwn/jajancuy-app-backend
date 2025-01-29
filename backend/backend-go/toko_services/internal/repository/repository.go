package repository

import (
	"database/sql"
	"errors"
	"toko_services/internal/domain"
)

// TokoRepository implements domain.TokoDomain
type TokoRepository struct {
	db *sql.DB
}

// NewTokoRepository creates a new instance of TokoRepository
func NewTokoRepository(db *sql.DB) domain.TokoDomain {
	return &TokoRepository{db: db}
}

// CreateToko adds a new store to the database
func (r *TokoRepository) CreateToko(toko domain.Toko) (int, error) {
	query := "INSERT INTO toko (name, description, address, owner_id) VALUES ($1, $2, $3, $4) RETURNING id"
	var id int
	err := r.db.QueryRow(query, toko.Name, toko.Description, toko.Address, toko.OwnerID).Scan(&id)
	if err != nil {
		return 0, err
	}
	return id, nil
}

// GetTokoByID retrieves a store by its ID
func (r *TokoRepository) GetTokoByID(id int) (*domain.Toko, error) {
	query := "SELECT id, name, description, address, owner_id FROM toko WHERE id = $1"
	row := r.db.QueryRow(query, id)

	var toko domain.Toko
	err := row.Scan(&toko.ID, &toko.Name, &toko.Description, &toko.Address, &toko.OwnerID)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil // No data found
		}
		return nil, err
	}
	return &toko, nil
}

// GetAllToko retrieves all stores
func (r *TokoRepository) GetAllToko() ([]domain.Toko, error) {
	query := "SELECT id, name, description, address, owner_id FROM toko"
	rows, err := r.db.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tokos []domain.Toko
	for rows.Next() {
		var toko domain.Toko
		err := rows.Scan(&toko.ID, &toko.Name, &toko.Description, &toko.Address, &toko.OwnerID)
		if err != nil {
			return nil, err
		}
		tokos = append(tokos, toko)
	}
	return tokos, nil
}

// UpdateToko updates an existing store
func (r *TokoRepository) UpdateToko(toko domain.Toko) error {
	query := "UPDATE toko SET name = $1, description = $2, owner_id = $3 WHERE id = $4"
	_, err := r.db.Exec(query, toko.Name, toko.Description, toko.Address, toko.OwnerID, toko.ID)
	return err
}

// DeleteToko deletes a store by its ID
func (r *TokoRepository) DeleteToko(id int) error {
	query := "DELETE FROM toko WHERE id = $1"
	_, err := r.db.Exec(query, id)
	return err
}
