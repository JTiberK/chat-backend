Paso 1: Configurar el backend de Flask
Crear un nuevo directorio para el proyecto Python

```bash
mkdir gemini-chat-backend
cd gemini-chat-backend
python -m venv venv
```


 > [!CAUTION]
 > Para activar el entorno virtual en bash

```
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

```diff

diff | Para activar un entorno virtual en PowerShell, debes usar el comando específico del entorno
diff | virtual que hayas creado. Por ejemplo, si estás trabajando con Python y has creado un entorno virtual 
diff | usando `venv`, puedes activarlo con el siguiente comando:

```

```diff powershell
+ .\nombre_del_entorno\Scripts\Activate.ps1
```
Asegúrate de reemplazar `nombre_del_entorno` con el nombre de tu entorno virtual.

Si tienes problemas para ejecutar el script debido a restricciones de ejecución en PowerShell, puedes cambiar la política de ejecución con el siguiente comando:


```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Esto permitirá ejecutar scripts firmados localmente.