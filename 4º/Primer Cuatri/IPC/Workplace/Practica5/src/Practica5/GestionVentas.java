package Practica5;

import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.Font;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.JToolBar;
import javax.swing.ListSelectionModel;
import javax.swing.table.DefaultTableModel;

import dominio.Transaccion;

import java.awt.Color;

public class GestionVentas {
	
	// ArrayList para guardar las transacciones
	private ArrayList<Transaccion> transacciones = new ArrayList<Transaccion>();
	private int indiceSeleccionado = -1; // para saber qué fila está seleccionada
	
	// Componentes de la interfaz
	private JButton btnGuardartB;
	private JButton btnEliminar;
	private JButton btnDeseleccionar;
	private JFrame FormularioDeTransacciones;
	private JToolBar tbBarraHerramientas;
	private JLabel lblBarraEstado;
	
	// La tabla y su modelo
	private JTable tabla;
	private DefaultTableModel modeloTabla;
	
	// Los campos de texto del formulario
	private JTextField txtId;
	private JTextField txtFecha;
	private JTextField txtEmpleado;
	private JTextField txtJuego;
	private JTextField txtCantidad;
	private JComboBox<String> cbTipo;
	private JTextField txtTotal;
	
	private JPanel pnlPanelFicha = new JPanel();

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					GestionVentas window = new GestionVentas();
					window.FormularioDeTransacciones.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	public GestionVentas() {
		initialize();
	}

	private void initialize() {
		// Configuración del frame principal
		FormularioDeTransacciones = new JFrame();
		FormularioDeTransacciones.setResizable(false);
		FormularioDeTransacciones.setTitle("Formulario de Transacciones");
		FormularioDeTransacciones.setBounds(100, 100, 700, 450);
		FormularioDeTransacciones.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		// Toolbar arriba
		tbBarraHerramientas = new JToolBar();
		FormularioDeTransacciones.getContentPane().add(tbBarraHerramientas, BorderLayout.NORTH);

		// Barra de estado abajo
		lblBarraEstado = new JLabel("Bienvenido");
		lblBarraEstado.setFont(new Font("Tahoma", Font.PLAIN, 11));
		FormularioDeTransacciones.getContentPane().add(lblBarraEstado, BorderLayout.SOUTH);
	
		// Botones del toolbar
		btnGuardartB = new JButton("Guardar");
		tbBarraHerramientas.add(btnGuardartB);
		btnGuardartB.setToolTipText("Guardar");
		
		JButton btnBuscar = new JButton("Buscar por ID");
		tbBarraHerramientas.add(btnBuscar);
		
		btnDeseleccionar = new JButton("Deseleccionar");
		btnDeseleccionar.setEnabled(false); // empieza deshabilitado
		tbBarraHerramientas.add(btnDeseleccionar);
		
		// Panel del formulario
		FormularioDeTransacciones.getContentPane().add(pnlPanelFicha, BorderLayout.CENTER);
		pnlPanelFicha.setLayout(null); // posicionamiento absoluto

		// Campo ID
		JLabel lblIdDeTransaccion = new JLabel("ID de transacción");
		lblIdDeTransaccion.setBounds(10, 10, 120, 14);
		pnlPanelFicha.add(lblIdDeTransaccion);
		
		txtId = new JTextField();
		txtId.setColumns(10);
		txtId.setBounds(140, 8, 100, 20);
		pnlPanelFicha.add(txtId);
		
		// Campo Fecha
		JLabel lblFecha = new JLabel("Fecha (yyyy-MM-dd)");
		lblFecha.setBounds(10, 36, 120, 14);
		pnlPanelFicha.add(lblFecha);
		
		txtFecha = new JTextField();
		txtFecha.setText(LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd")));
		txtFecha.setBounds(140, 34, 100, 20);
		pnlPanelFicha.add(txtFecha);
		
		// Campo Empleado
		JLabel lblEmpleadoResponsable = new JLabel("Empleado ID");
		lblEmpleadoResponsable.setBounds(10, 62, 120, 14);
		pnlPanelFicha.add(lblEmpleadoResponsable);
		
		txtEmpleado = new JTextField();
		txtEmpleado.setBounds(140, 60, 100, 20);
		pnlPanelFicha.add(txtEmpleado);
		
		// Campo Videojuego
		JLabel lblVideojuegoVendido = new JLabel("Videojuego");
		lblVideojuegoVendido.setBounds(10, 88, 120, 14);
		pnlPanelFicha.add(lblVideojuegoVendido);
		
		txtJuego = new JTextField();
		txtJuego.setBounds(140, 86, 140, 20);
		pnlPanelFicha.add(txtJuego);
		
		// Campo Cantidad
		JLabel lblCantidad = new JLabel("Cantidad");
		lblCantidad.setBounds(349, 10, 91, 14);
		pnlPanelFicha.add(lblCantidad);
		
		txtCantidad = new JTextField();
		txtCantidad.setBounds(494, 8, 120, 20);
		pnlPanelFicha.add(txtCantidad);
		
		// ComboBox Tipo
		JLabel lblTipo = new JLabel("Tipo de Operación");
		lblTipo.setBounds(349, 36, 111, 14);
		pnlPanelFicha.add(lblTipo);
		
		cbTipo = new JComboBox<>(new String[]{"Venta", "Entrada", "Salida"});
		cbTipo.setBounds(494, 33, 120, 20);
		pnlPanelFicha.add(cbTipo);

		// Campo Total
		JLabel lblTotal = new JLabel("Total (€)");
		lblTotal.setBounds(349, 62, 91, 14);
		pnlPanelFicha.add(lblTotal);

		txtTotal = new JTextField();
		txtTotal.setBounds(494, 60, 120, 20);
		pnlPanelFicha.add(txtTotal);

		// Botones de acción
		JButton btnGuardarBot = new JButton("Guardar");
		btnGuardarBot.setBounds(140, 120, 120, 25);
		pnlPanelFicha.add(btnGuardarBot);

		JButton btnNuevo = new JButton("Nuevo/Limpiar");
		btnNuevo.setBounds(311, 120, 140, 25);
		pnlPanelFicha.add(btnNuevo);
		
		btnEliminar = new JButton("Eliminar");
		btnEliminar.setBounds(494, 120, 120, 25);
		btnEliminar.setEnabled(false); // al principio no hay nada seleccionado
		pnlPanelFicha.add(btnEliminar);
		
		JButton btnActualizar = new JButton("Actualizar tabla");
		btnActualizar.setBounds(140, 155, 120, 25);
		pnlPanelFicha.add(btnActualizar);
		
		JButton btnSalir = new JButton("Salir");
		btnSalir.setBounds(494, 155, 120, 25);
		pnlPanelFicha.add(btnSalir);
		
		// Panel de la tabla
		JPanel panelTabla = new JPanel();
		panelTabla.setBackground(new Color(255, 255, 255));
		panelTabla.setBounds(10, 190, 660, 180);
		pnlPanelFicha.add(panelTabla);
		
		// tabla con las columnas
		modeloTabla = new DefaultTableModel(
			new String[]{"ID", "Fecha", "Empleado", "Juego", "Cantidad", "Tipo", "Total"}, 
			0
		) {
			@Override
			public boolean isCellEditable(int row, int column) {
				return false; 
			}
		};
		
		tabla = new JTable(modeloTabla);
		tabla.setSelectionMode(ListSelectionModel.SINGLE_SELECTION); // solo una fila a la vez
		
		panelTabla.setLayout(new BorderLayout());
		panelTabla.add(new JScrollPane(tabla), BorderLayout.CENTER);

		
		
		// Botón salir
		btnSalir.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				System.exit(0);
			}
		});
		
		// seleccion de fila
		tabla.getSelectionModel().addListSelectionListener(e -> {
			if (!e.getValueIsAdjusting()) {
				int fila = tabla.getSelectedRow();
				if (fila >= 0 && fila < transacciones.size()) {
					indiceSeleccionado = fila;
					cargarDatosEnFormulario(transacciones.get(fila));
					btnDeseleccionar.setEnabled(true);
					btnEliminar.setEnabled(true);
					lblBarraEstado.setText("Transacción seleccionada (fila " + fila + ")");
				}
			}
		});
		
		//  guardar 
		MouseAdapter guardarHandler = new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
				guardarTransaccion();
			}
		};
		
		btnGuardartB.addMouseListener(guardarHandler);
		btnGuardarBot.addMouseListener(guardarHandler);
		
		// Buscar por ID
		btnBuscar.addActionListener(e -> {
			buscarPorId();
		});
		
		// Eliminar
		btnEliminar.addActionListener(e -> {
			eliminarTransaccion();
		});
		
		// Deseleccionar
		btnDeseleccionar.addActionListener(e -> {
			tabla.clearSelection();
			indiceSeleccionado = -1;
			btnDeseleccionar.setEnabled(false);
			btnEliminar.setEnabled(false);
			lblBarraEstado.setText("Deseleccionado");
		});
		
		// Actualizar tabla
		btnActualizar.addActionListener(e -> {
			refrescarTabla();
			lblBarraEstado.setText("Tabla actualizada");
		});
		
		// Nuevo/Limpiar
		btnNuevo.addActionListener(e -> {
			limpiar();
			tabla.clearSelection();
			indiceSeleccionado = -1;
			btnDeseleccionar.setEnabled(false);
			btnEliminar.setEnabled(false);
			lblBarraEstado.setText("Formulario limpio");
		});
	}

	//guardar o actualizar una transacción
	void guardarTransaccion() {
		try {
			// Leo los datos del formulario
			int id = Integer.parseInt(txtId.getText().trim());
			
			// Compruebo si ya existe ese ID (solo si es nueva)
			if (indiceSeleccionado < 0 && yaExisteId(id)) {
				JOptionPane.showMessageDialog(FormularioDeTransacciones, 
					"Ya existe una transacción con ese ID.", "Error", JOptionPane.ERROR_MESSAGE);
				return;
			}
			
			DateTimeFormatter formato = DateTimeFormatter.ofPattern("yyyy-MM-dd");
			LocalDate fecha = LocalDate.parse(txtFecha.getText().trim(), formato);
			int empleado = Integer.parseInt(txtEmpleado.getText().trim());
			String juego = txtJuego.getText().trim();
			int cantidad = Integer.parseInt(txtCantidad.getText().trim());
			String tipo = (String) cbTipo.getSelectedItem();
			String totalTexto = txtTotal.getText().trim().replace(',', '.');
			BigDecimal total = new BigDecimal(totalTexto);
			
			if (indiceSeleccionado >= 0) {
				// Si hay algo seleccionado, actualizo
				Transaccion t = transacciones.get(indiceSeleccionado);
				t.setId(id);
				t.setFecha(fecha);
				t.setEmpleadoResponsable(empleado);
				t.setNombreJuego(juego);
				t.setCantidad(cantidad);
				t.setTipo(tipo);
				t.setTotal(total);
				lblBarraEstado.setText("Transacción actualizada");
			} else {
				// Si no, creo una nueva
				Transaccion nueva = new Transaccion(id, fecha, empleado, juego, cantidad, tipo, total);
				transacciones.add(nueva);
				lblBarraEstado.setText("Transacción añadida");
			}
			
			refrescarTabla();
		} catch (Exception ex) {
			JOptionPane.showMessageDialog(FormularioDeTransacciones, 
				"Error: " + ex.getMessage(), "Validación", JOptionPane.ERROR_MESSAGE);
		}
	}

	// Actualiza la tabla con todos los datos del ArrayList
	private void refrescarTabla() {
		modeloTabla.setRowCount(0); 
		for (Transaccion t : transacciones) {
			modeloTabla.addRow(new Object[]{
				t.getId(),
				t.getFecha(),
				t.getEmpleadoResponsable(),
				t.getNombreJuego(),
				t.getCantidad(),
				t.getTipo(),
				t.getTotal()
			});
		}
	}

	// Carga los datos de una transacción en el formulario
	private void cargarDatosEnFormulario(Transaccion t) {
		DateTimeFormatter formato = DateTimeFormatter.ofPattern("yyyy-MM-dd");
		txtId.setText(String.valueOf(t.getId()));
		txtFecha.setText(t.getFecha().format(formato));
		txtEmpleado.setText(String.valueOf(t.getEmpleadoResponsable()));
		txtJuego.setText(t.getNombreJuego());
		txtCantidad.setText(String.valueOf(t.getCantidad()));
		cbTipo.setSelectedItem(t.getTipo());
		txtTotal.setText(t.getTotal().toPlainString());
	}

	// Busca una transacción por ID y la selecciona en la tabla
	private void buscarPorId() {
		try {
			int id = Integer.parseInt(txtId.getText().trim());
			int posicion = -1;
			
			// Busco el índice en el ArrayList
			for (int i = 0; i < transacciones.size(); i++) {
				if (transacciones.get(i).getId() == id) {
					posicion = i;
					break;
				}
			}
			
			if (posicion >= 0) {
				tabla.setRowSelectionInterval(posicion, posicion);
				tabla.scrollRectToVisible(tabla.getCellRect(posicion, 0, true));
				lblBarraEstado.setText("Encontrada transacción ID " + id);
			} else {
				JOptionPane.showMessageDialog(FormularioDeTransacciones, 
					"No se encontró transacción con ID: " + id);
			}
		} catch (NumberFormatException ex) {
			JOptionPane.showMessageDialog(FormularioDeTransacciones, 
				"El ID debe ser numérico");
		}
	}

	// Elimina la transacción seleccionada
	private void eliminarTransaccion() {
		if (indiceSeleccionado >= 0) {
			int confirmar = JOptionPane.showConfirmDialog(FormularioDeTransacciones,
				"¿Eliminar transacción?", "Confirmar", JOptionPane.YES_NO_OPTION);
			if (confirmar == JOptionPane.YES_OPTION) {
				transacciones.remove(indiceSeleccionado);
				refrescarTabla();
				limpiar();
				indiceSeleccionado = -1;
				tabla.clearSelection();
				btnDeseleccionar.setEnabled(false);
				btnEliminar.setEnabled(false);
				lblBarraEstado.setText("Transacción eliminada");
			}
		}
	}

	// Comprueba si ya existe un ID
	private boolean yaExisteId(int id) {
		for (Transaccion t : transacciones) {
			if (t.getId() == id) {
				return true;
			}
		}
		return false;
	}

	// Limpia el formulario
	private void limpiar() {
		DateTimeFormatter formato = DateTimeFormatter.ofPattern("yyyy-MM-dd");
		txtId.setText("");
		txtFecha.setText(LocalDate.now().format(formato));
		txtEmpleado.setText("");
		txtJuego.setText("");
		txtCantidad.setText("");
		cbTipo.setSelectedIndex(0);
		txtTotal.setText("");
	}
}
