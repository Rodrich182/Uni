package dominio;

import java.math.BigDecimal;
import java.time.LocalDate;

public class Transaccion {
    private int id;
    private LocalDate fecha;
    private int empleadoResponsable;
    private String nombreJuego;
    private int cantidad;
    private String tipo; // o TransactionType si es un enum
    private BigDecimal total;

    public Transaccion(int id, LocalDate fecha, int empleadoResponsable, String nombreJuego, int cantidad, String tipo, BigDecimal total) {
        this.id = id;
        this.fecha = fecha;
        this.empleadoResponsable = empleadoResponsable;
        this.nombreJuego = nombreJuego;
        this.cantidad = cantidad;
        this.tipo = tipo;
        this.total = total;
    }

    public int getId()
    {
    	return this.id; 
    }
    public void setId(int id) {
    	this.id = id; 
    }

    public LocalDate getFecha() {
    	return this.fecha; 
    }
    public void setFecha(LocalDate fecha) {
    	this.fecha = fecha; 
    }

    public int getEmpleadoResponsable() { 
    	return this.empleadoResponsable; 
    }
    public void setEmpleadoResponsable(int empleadoResponsable) { 
    	this.empleadoResponsable = empleadoResponsable; 
    }

    public String getNombreJuego() {
    	return this.nombreJuego; 
    }
    public void setNombreJuego(String nombreJuego) { 
    	this.nombreJuego = nombreJuego; 
    }

    public int getCantidad() { 
    	return this.cantidad; 
    }
    public void setCantidad(int cantidad) { 
    	this.cantidad = cantidad; 
    }

    public String getTipo() { 
    	return this.tipo; 
    }
    public void setTipo(String tipo) { 
    	this.tipo = tipo; 
    }

    public BigDecimal getTotal() {
    	return this.total; 
    }
    public void setTotal(BigDecimal total) { 
    	this.total = total; 
    }
}
