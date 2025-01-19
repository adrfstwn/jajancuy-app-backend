package domain

type Toko struct {
	ID          int
	Name        string
	Description string
	OwnerID     int
}

// TokoService defines the interface for accessing Toko data
type TokoDomain interface {
	CreateToko(toko Toko) (int, error) // Add a new store, returning the ID
	GetTokoByID(id int) (*Toko, error) // Get a store by its ID
	GetAllToko() ([]Toko, error)       // Get all stores
	UpdateToko(toko Toko) error        // Update an existing store
	DeleteToko(id int) error           // Delete a store by its ID
}
