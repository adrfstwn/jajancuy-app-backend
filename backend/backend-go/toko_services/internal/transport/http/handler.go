package http

import (
	"net/http"
	"strconv"
	"toko_services/internal/domain"
	"toko_services/internal/service"

	"github.com/gin-gonic/gin"
)

type TokoHandler struct {
	service *service.TokoService
}

func NewTokoHandler(service *service.TokoService) *TokoHandler {
	return &TokoHandler{service: service}
}

func (h *TokoHandler) CreateToko(c *gin.Context) {
	var toko domain.Toko
	if err := c.ShouldBindJSON(&toko); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	id, err := h.service.CreateToko(toko, c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusCreated, gin.H{"id": id})
}

func (h *TokoHandler) GetAllToko(c *gin.Context) {
	tokos, err := h.service.GetAllToko()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, tokos)
}

func (h *TokoHandler) GetTokoByID(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid ID"})
		return
	}
	toko, err := h.service.GetTokoByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, toko)
}

func (h *TokoHandler) UpdateToko(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid ID"})
		return
	}
	var toko domain.Toko
	if err := c.ShouldBindJSON(&toko); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	toko.ID = id
	if err := h.service.UpdateToko(toko); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "Toko updated successfully"})
}

func (h *TokoHandler) DeleteToko(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid ID"})
		return
	}
	if err := h.service.DeleteToko(id); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"message": "Toko deleted successfully"})
}
