package logger

import (
	"fmt"
	"log"
	"os"
	"time"
)

// Logger interface, provides different logging levels
type Logger interface {
	Info(message string)
	Warn(message string)
	Error(message string)
	Fatal(message string)
}

// SimpleLogger implements the Logger interface using the standard library log
type SimpleLogger struct {
	logger *log.Logger
}

// New creates a new logger instance
func New() Logger {
	// Setup logging to log to both file and console
	file, err := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		fmt.Println("Error opening log file:", err)
		os.Exit(1)
	}

	// Return a SimpleLogger with both console and file output
	return &SimpleLogger{
		logger: log.New(file, "", log.LstdFlags),
	}
}

// Info logs an informational message
func (l *SimpleLogger) Info(message string) {
	l.logger.SetPrefix("[INFO] ")
	l.logger.Println(message)
}

// Warn logs a warning message
func (l *SimpleLogger) Warn(message string) {
	l.logger.SetPrefix("[WARN] ")
	l.logger.Println(message)
}

// Error logs an error message
func (l *SimpleLogger) Error(message string) {
	l.logger.SetPrefix("[ERROR] ")
	l.logger.Println(message)
}

// Fatal logs a fatal error message and exits the application
func (l *SimpleLogger) Fatal(message string) {
	l.logger.SetPrefix("[FATAL] ")
	l.logger.Println(message)
	os.Exit(1)
}

// LogRequest logs HTTP request details
func LogRequest(method, path string, status int, duration time.Duration) {
	log.Printf("[REQUEST] %s %s %d %s\n", method, path, status, duration)
}
