package main

import (
	"toko_services/internal/app"
	"toko_services/internal/repository"
	"toko_services/internal/service"
	"toko_services/internal/transport/http"
	"toko_services/pkg/logger"
	"toko_services/pkg/middleware"

	"os"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {

	app.LoadEnv()

	log := logger.New()

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default to 8080 if not set
	}

	log.Info("Application Staring...")

	// Initialize Gin Router
	r := gin.Default()

	r.Use(cors.Default())

	// DB Connection
	db, err := repository.DatabaseConnection()
	if err != nil {
		log.Fatal("Failed to connect to database: " + err.Error())
	}
	defer db.Close()

	// Initialize Repo, Service, Handler
	tokoRepo := repository.NewTokoRepository(db)
	tokoService := service.NewTokoService(tokoRepo)
	tokoHandler := http.NewTokoHandler(tokoService)

	// Routes
	api := r.Group("/api/v1")
	{
		tokoRoutes := api.Group("/toko", middleware.JwtMiddleware())
		{
			tokoRoutes.POST("/", tokoHandler.CreateToko)
			tokoRoutes.GET("/", tokoHandler.GetAllToko)
			tokoRoutes.GET("/:id", tokoHandler.GetTokoByID)
			tokoRoutes.PUT("/:id", tokoHandler.UpdateToko)
			tokoRoutes.DELETE("/:id", tokoHandler.DeleteToko)
		}
	}

	// Run the server
	if err := r.Run(":" + port); err != nil {
		log.Fatal("Failed to run server: " + err.Error())
	}

}
