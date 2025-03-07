//const ConectorPluginV3 = (() => {
    // class Operacion {
    //     public nombre: string
    //     public argumentos: any
    //     constructor(nombre, argumentos) {
    //       this.nombre = nombre;
    //       this.argumentos = argumentos;
    //     }
    // }
    
    // class ConectorPlugin {

    //     static URL_PLUGIN_POR_DEFECTO = 'http://localhost:5108';
    //     static Operacion = Operacion;
    //     public ruta: string
    //     public operaciones: Operacion[]
    //     constructor() {
    //         this.ruta = ConectorPlugin.URL_PLUGIN_POR_DEFECTO;
    //         this.operaciones = [];
    //         return this;
    //     }
    //     // size(x,y){
    //     //     this.operaciones.push(new Operacion("size",Array.from(arguments)))
    //     //     return this
    //     // }
        
    //     text( content:string,
    //          size: "Normal"|
    //     "DoubleHeight"|
    //     "DoubleWidth"|
    //     "DoubleBoth", 
    //     alignment:"Left"|
    //     "Center"|
    //     "Right", 
    //     font:"FontA"|
    //     "FontB", 
    //     style:"Bold"|"Underline"|"B&U"|"None") {
    //         this.operaciones.push(new Operacion("text", [content,TextSize[size],Alignment[alignment],
    //         FontType[font],style]));
    //         return this;
    //     }
    
            
    //     setPrinter(name:string) {
    //         this.operaciones.push(new Operacion("setPrinter", Array.from(arguments)));
    //         return this;
    //     }
    

    //     image(imagePath) {
    //         this.operaciones.push(new Operacion("image", Array.from(arguments)));
    //         return this;
    //     }

    //     async print(){
    //         fetch('http://localhost:5108/print', {
    //             method: 'POST',  // Specify the HTTP method
    //             headers: {
    //                 'Content-Type': 'application/json',  // Set the content type header to JSON
    //             },
    //             body: JSON.stringify({ operations: this.operaciones })  // Convert your data to a JSON string
    //         })
    //         .then(async response => console.log(await response.text()))  // Parse the JSON response
    //         .catch((error) => {
    //             console.error('Error:', error);  // Handle errors
    //         });
    //     }
    // }

    class Operacion {
        constructor(nombre, argumentos) {
            this.nombre = nombre;
            this.argumentos = argumentos;
        }
    }
    
    class ConectorPlugin {
    
        static URL_PLUGIN_POR_DEFECTO = 'http://localhost:5108';
        static Operacion = Operacion;
    
        constructor() {
            this.ruta = ConectorPlugin.URL_PLUGIN_POR_DEFECTO;
            this.operaciones = [];
            return this;
        }
    
        text(content, size, alignment, font, style) {
            this.operaciones.push(new Operacion("text", [
                content,
                TextSize[size],
                Alignment[alignment],
                FontType[font],
                style
            ]));
            return this;
        }
    
        setPrinter(name) {
            this.operaciones.push(new Operacion("setPrinter", Array.from(arguments)));
            return this;
        }
    
        image(imagePath) {
            this.operaciones.push(new Operacion("image", Array.from(arguments)));
            return this;
        }
    
        async print() {
            fetch('http://localhost:5000/print', {
                method: 'POST',  // Specify the HTTP method
                headers: {
                    'Content-Type': 'application/json',  // Set the content type header to JSON
                },
                body: JSON.stringify({ operations: this.operaciones })  // Convert your data to a JSON string
            })
            .then(async response => console.log(await response.text()))  // Parse the response
            .catch((error) => {
                console.error('Error:', error);  // Handle errors
            });
        }
    }
    
    // You will also need to define the enums or objects used in the `text` function
    // such as TextSize, Alignment, FontType, etc., or replace them with actual values.
    
    const Alignment = {
        "Left": 0,
        "Center": 1,
        "Right": 2
    };
    
    const FontType = {
        "FontA": 0,
        "FontB": 1
    };
    
    const TextSize = {
        "Normal": 0,
        "DoubleHeight": 1,
        "DoubleWidth": 2,
        "DoubleBoth": 3
    };
    
//})();

const aux=new ConectorPlugin()
aux.
setPrinter('IMP1')
.text("test",'DoubleHeight','Center','FontA','None')
.print()
