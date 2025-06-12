# 🤝 CONTRIBUTING.md

## 🙋‍♂️ ¿Quién puede contribuir?

Este es un proyecto **privado e interno**. Por ahora, solo miembros autorizados (Luis A. y equipo) pueden contribuir.

---

## 📝 Reglas básicas

✅ Mantener un código limpio y ordenado✅ Comentar adecuadamente las funciones y los cambios relevantes✅ No hacer commit de:

- `crm.db` (DB local de pruebas)
- `venv/`
- Archivos `.DS_Store` de macOS

✅ Siempre actualizar los siguientes documentos si el cambio lo amerita:

- `docs/CLIENT_MASTER_DATABASE.md`
- `docs/PROJECT_LOGIC.md`
- `README.md`

---

## 🗂️ Flujo de trabajo con Git

```bash
# 1️⃣ Clonar el repo (si es la primera vez)
git clone https://github.com/laguileracl/fastapi-crm-cxc.git
cd fastapi-crm-cxc

# 2️⃣ Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3️⃣ Antes de trabajar: traer últimos cambios
git pull origin master

# 4️⃣ Trabajar en tu feature
git status
git add archivos_modificados
git commit -m "feat: breve descripción de lo que hiciste"
git push origin master
```
