import datetime

class logger:
    
    _instancia = None
    
    def __new__(cls):
        
        if cls._instancia is None:
            
            cls._instancia = super().__new__(cls)
            
            cls._instancia._log = []
            
        return cls._instancia
    
    def _registrar(self, nivel, mensaje):
        
        hora = datetime.datetime.now().strftime("%d/%m/%/y %H:%M:%S")
        
        entrada = {
            
            "hora": hora,
            "nivel": nivel,
            "mensaje": mensaje
        }
        
        self._logs.append(entrada)
        
        
    def info(self, mensaje):
            
        self._registrar("INFO", mensaje)
            
    def warning(self, mensaje):
            
        self._registrar("WARNING", mensaje)
            
    def error(self, mensaje):
            
        self._registrar("ERROR", mensaje)
    
    
    def mostrar_logs(self):
        
        print("\n ==================== HISTORIAL DE SISTEMA =======================")
        
        if len(self._logs) == 0:
            
            print("No existen registros.")
            
            return
        for log in self._logs:
            print(
                f"[{log['hora']}] {log['nivel']:8} {log['mensaje']} "
            )
    
    def limpiar(self):
        
        self._long.clear()
        
        print("\nHistorial eliminado correctamente.")