import javax.swing.*;

import java.awt.*;
import java.awt.datatransfer.*;
import java.awt.dnd.*;

import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileWriter;
import java.io.BufferedWriter;

import java.util.List;

import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class Practica0 extends JFrame {

    private JTextPane areaArchivo;
    private JPanel menu;
    private File archivo = null;

    public Practica0(){
        //Configuración inicial del frame
        setTitle("Cifrado de Archivos");
        setSize(800, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        //Para el panel en donde se soltará el archivo
        areaArchivo = new JTextPane();
        areaArchivo.setText("Arrastra el archivo aquí o haz clic para cargar un archivo.");
        //Para centrar el contenido del textPane
        StyledDocument doc = areaArchivo.getStyledDocument();
        SimpleAttributeSet center = new SimpleAttributeSet();
        StyleConstants.setAlignment(center, StyleConstants.ALIGN_CENTER);
        doc.setParagraphAttributes(0, doc.getLength(), center, false);
        
        areaArchivo.setFont(new Font(Font.DIALOG_INPUT, Font.PLAIN, 18));
        areaArchivo.setEditable(false); //Para que no se pueda editar el textArea
        areaArchivo.setBorder(BorderFactory.createLineBorder(Color.BLACK));
        // areaArchivo.setLineWrap(true); //Para que el texto se ajuste al tamaño del area
        // areaArchivo.setWrapStyleWord(true); //Para que no se corte una palabra a la mitad
        areaArchivo.setPreferredSize(new Dimension(300,100));
        areaArchivo.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));

        new DropTarget(areaArchivo, new DropTargetListener() {
            public void dragEnter(DropTargetDragEvent dtde) {}
            public void dragOver(DropTargetDragEvent dtde) {}
            public void dropActionChanged(DropTargetDragEvent dtde) {}
            public void dragExit(DropTargetEvent dte) {}
            public void drop(DropTargetDropEvent dtde){
                try{
                    dtde.acceptDrop(DnDConstants.ACTION_COPY);
                    Transferable t = dtde.getTransferable();
                    List<File> listaArchivos = (List<File>) t.getTransferData(DataFlavor.javaFileListFlavor);

                    if(listaArchivos.size() > 0 ){
                        archivo = listaArchivos.get(0);
                        String nombreArchivo = archivo.getName().toLowerCase();

                        //Validamos que solo sean archivos txt o bmp
                        if(nombreArchivo.endsWith(".txt") || nombreArchivo.endsWith(".bmp")){
                            MostrarArchivoCargado(archivo);
                        }else{
                            areaArchivo.setText("Formato no soportado, solo .txt o .bmp.\nSube un archivo válido.");
                        }
                    }
                }catch(Exception e){
                    e.printStackTrace();
                }
            }
        });

        areaArchivo.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent mEvt) {
                archivo = cargarArchivo();
            }
        });

        add(new JScrollPane(areaArchivo), BorderLayout.CENTER);

        //Para el menu
        menu = new JPanel();
        menu.setLayout(new GridLayout(3,1));

        JButton cifrarButton = new JButton("Cifrar");
        cifrarButton.setFont(new Font(Font.DIALOG_INPUT, Font.BOLD, 16));
        cifrarButton.addActionListener(e -> cifrarDescifrarArchivo(archivo, true));

        JButton descifrarButton = new JButton("Descifrar");
        descifrarButton.setFont(new Font(Font.DIALOG_INPUT, Font.BOLD, 16));
        descifrarButton.addActionListener(e -> cifrarDescifrarArchivo(archivo, false));

        JButton salirButton = new JButton("Salir");
        salirButton.setFont(new Font(Font.DIALOG_INPUT, Font.BOLD, 16));
        salirButton.addActionListener(e -> System.exit(0));

        menu.add(cifrarButton);
        menu.add(descifrarButton);
        menu.add(salirButton);

        add(menu, BorderLayout.EAST);        
    }

    //Metodo para mostrar el contenido del archivo dependiendo si es txt o bmp
    private void MostrarArchivoCargado(File archivo){
        String nombreArchivo = archivo.getName().toLowerCase();

        if(nombreArchivo.endsWith(".txt")){
            MostrarArchivoTxt(archivo);
        }else if(nombreArchivo.endsWith(".bmp")){
            MostrarArchivoBmp(archivo);
        }
    }

    private void MostrarArchivoTxt(File archivo){
        try (BufferedReader lectura = new BufferedReader(new FileReader(archivo))){
            areaArchivo.setText("");
            String l;
            while((l = lectura.readLine()) != null){
                areaArchivo.setText(areaArchivo.getText() + l + "\n");
            }
        }catch(Exception e){
            areaArchivo.setText("Error al mostrar el archivo");
            e.printStackTrace();
        }
    }

    private void MostrarArchivoBmp(File archivo){
        try{
            BufferedImage img = ImageIO.read(archivo);
            ImageIcon icono = new ImageIcon(img.getScaledInstance(areaArchivo.getWidth(), areaArchivo.getHeight(), Image.SCALE_DEFAULT)); //Con escala
            // ImageIcon icono = new ImageIcon(img); //Sin escala
            JLabel labelImagen = new JLabel(icono);

            areaArchivo.setText("");
            areaArchivo.insertComponent(labelImagen);
        }catch(Exception e){
            areaArchivo.setText("Error al mostrar la imagen.");
            e.printStackTrace();
        }
    }

    //Para cargar un archivo si no se desea arrastrar
    private File cargarArchivo(){
        JFileChooser chooser = new JFileChooser();
        int valor = chooser.showOpenDialog(this);
        if(valor == JFileChooser.APPROVE_OPTION){
            File archivo = chooser.getSelectedFile();
            String nombreArchivo = archivo.getName().toLowerCase();

            if(nombreArchivo.endsWith(".txt") || nombreArchivo.endsWith(".bmp")){
                MostrarArchivoCargado(archivo);
                return archivo;
            }else{
                areaArchivo.setText("Formato no soportado, solo .txt o .bmp.\nSube un archivo válido.");
                return null;
            }
        }
        return null;
    }

    private void cifrarDescifrarArchivo(File archivo, boolean cifrar){
        //Checamos si un archivo ha sido cargado
        if(archivo == null){
            areaArchivo.setText("No se ha cargado un archivo.\nArrastra el archivo aquí o haz clic para cargar un archivo.");
            return;
        }

        //Checamos si el archivo es txt o bmp
        String nombreArchivo = archivo.getName().toLowerCase();
        if(nombreArchivo.endsWith(".txt")){ //Es archivo txt
            int desplazamientos = validarDesplazamientos(true);

            //Ciframos el archivo
            String textoNuevo = "";
            for(char c: (areaArchivo.getText()).toCharArray()){
                textoNuevo += (char)(cifrar ? c + desplazamientos : (c != 10 ? c - desplazamientos: c)); //10 es el salto de linea
            }

            //Guardamos el nuevo texto en un archivo nuevo
            try{
                String nombreArchivoNuevo = "";
                File archivoNuevo = null;
                if(cifrar){ //Cifrado, entonces es "song_c.txt"
                    nombreArchivoNuevo = archivo.getName().replace(".txt", "_c.txt");
                    archivoNuevo = new File(archivo.getParent(), nombreArchivoNuevo);
                    archivoNuevo.createNewFile();
                }else{ //Descifrado, entonces es "song_c_d.txt"
                    nombreArchivoNuevo = archivo.getName().replace(".txt", "_d.txt");
                    archivoNuevo = new File(archivo.getParent(), nombreArchivoNuevo);
                    archivoNuevo.createNewFile();
                }

                try(BufferedWriter escribir = new BufferedWriter(new FileWriter(archivoNuevo))){
                    escribir.write(textoNuevo);
                    areaArchivo.setText("Archivo guardado como: " + nombreArchivoNuevo + "\n\nArrastra el archivo aquí o haz clic para cargar un archivo.");
                }catch(Exception e){
                    areaArchivo.setText("Error al guardar el archivo.\nArrastra el archivo aquí o haz clic para cargar un archivo.");
                    e.printStackTrace();
                }
            }catch(Exception e){
                areaArchivo.setText("Error al guardar el archivo.\nArrastra el archivo aquí o haz clic para cargar un archivo.");
                e.printStackTrace();
            }
        }else{ //Es imagen bmp
            //Pedimos los 3 desplazamientos para los 3 colores RGB
            int desplazamientosR = validarDesplazamientos(false), desplazamientosG = validarDesplazamientos(false), desplazamientosB = validarDesplazamientos(false);

            //Ciframos/Desciframos la imagen
            try{
                BufferedImage img = ImageIO.read(archivo);
                int ancho = img.getWidth();
                int alto = img.getHeight();
                int[][] coloresNuevos = new int[ancho][alto]; //Matriz para guardar los colores RGB para la nueva imagen

                for(int i = 0; i < ancho; i++){
                    for(int j = 0; j < alto; j++){
                        // int RGB = img.getRGB(i, j); //Metodo que regresa el color en RGB en un solo int
                        // int R = (RGB >> 16) & 0xFF; //Extraemos RED, >> 16 para mover 16 bits a la derecha y & 0xFF para obtener los ultimos 8 bits y limpiar los demas, se guardan en los ultimos 3 bytes del int
                        // int G = (RGB >> 8) & 0xFF; //Extraemos GREEN, >> 8 para mover 8 bits a la derecha
                        // int B = RGB & 0xFF; //Extraemos BLUE

                        //O bien, se puede hacer con el metodo Color.getRed(), Color.getGreen(), Color.getBlue()
                        Color color = new Color(img.getRGB(i, j));
                        int R = color.getRed();
                        int G = color.getGreen();
                        int B = color.getBlue();

                        //O bien, se puede hacer con el metodo getRGB(int x, int y) que regresa un arreglo de 3 elementos con los colores RGB
                        // int[] colores = new int[3];
                        // img.getRGB(i, j, colores);

                        //Colocamos los nuevos colores en la matriz y checamos que no se pase de 255 o menor a 0 cada uno de los colores
                        if(cifrar){
                            coloresNuevos[i][j] = new Color((R + desplazamientosR) > 255 ? (R + desplazamientosR) % 256 : (R + desplazamientosR), (G + desplazamientosG) > 255 ? (G + desplazamientosG) % 256 : (G + desplazamientosG), (B + desplazamientosB) > 255 ? (B + desplazamientosB) % 256 : (B + desplazamientosB)).getRGB();
                        }else{
                            coloresNuevos[i][j] = new Color((R - desplazamientosR) < 0 ? (255 + (R - desplazamientosR) % 256) : (R - desplazamientosR), (G - desplazamientosG) < 0 ? (255 + (G - desplazamientosG) % 256) : (G - desplazamientosG), (B - desplazamientosB) < 0 ? (255 + (B - desplazamientosB) % 256) : (B - desplazamientosB)).getRGB();
                        }
                    }
                }

                //Creamos la nueva imagen con los colores nuevos
                BufferedImage imgNueva = new BufferedImage(ancho, alto, BufferedImage.TYPE_INT_RGB);
                for(int i = 0; i < ancho; i++){
                    for(int j = 0; j < alto; j++){
                        imgNueva.setRGB(i, j, coloresNuevos[i][j]);
                    }
                }

                //Guardamos la nueva imagen
                String nombreNuevaImg = "";
                File archivoNuevaImg = null;
                if(cifrar){ //Cifrado, entonces es "img_c.bmp"
                    nombreNuevaImg = archivo.getName().replace(".bmp", "_c.bmp");
                    archivoNuevaImg = new File(archivo.getParent(), nombreNuevaImg);
                    archivoNuevaImg.createNewFile();
                }else{ //Descifrado, entonces es "img_c_d.bmp"
                    nombreNuevaImg = archivo.getName().replace(".bmp", "_d.bmp");
                    archivoNuevaImg = new File(archivo.getParent(), nombreNuevaImg);
                    archivoNuevaImg.createNewFile();
                }
                ImageIO.write(imgNueva, "bmp", archivoNuevaImg);
                areaArchivo.setText("Imagen guardada como: " + nombreNuevaImg + "\n\nArrastra el archivo aquí o haz clic para cargar un archivo.");

            }catch(Exception e){
                areaArchivo.setText("Error al Cifrar/Descifrar la imagen.");
                e.printStackTrace();
            }
        }
    }

    private int validarDesplazamientos(boolean txt){
        int desplazamientos = 0;

        //Pedimos la cantidad de desplazamientos
        desplazamientos = Integer.parseInt(JOptionPane.showInputDialog(this, "Ingresa la cantidad de desplazamientos " + (txt ? "(0-26): ": "(0-255)"), "Desplazamientos", JOptionPane.QUESTION_MESSAGE, null, null, 0).toString());

        while(desplazamientos < 0 || desplazamientos > (txt ? 26 : 255)){
            JOptionPane.showMessageDialog(this, "Ingresa un número entre 0 y " + (txt ? "26." : "255."), "Error", JOptionPane.ERROR_MESSAGE);
            desplazamientos = Integer.parseInt(JOptionPane.showInputDialog(this, "Ingresa la cantidad de desplazamientos " + (txt ? "(0-26): ": "(0-255)"), "Desplazamientos", JOptionPane.QUESTION_MESSAGE, null, null, 0).toString());
        }

        return desplazamientos;
    }

    public static void main(String[] args){
        SwingUtilities.invokeLater(() -> {
            Practica0 mainFrame = new Practica0();
            mainFrame.setVisible(true);
        });
    }

}

