import json
import model
import view

def handle_create_pet(handler, request_body):
    """
    Parses request body, validates input fields,
    calls the model to save the pet, and uses view to return the response.
    """
    try:
        if not request_body:
            view.render_error(handler, 400, "Corpo da requisição vazio.")
            return
        data = json.loads(request_body)
    except json.JSONDecodeError:
        view.render_error(handler, 400, "JSON inválido.")
        return

    # Extract fields with fallback defaults
    species = data.get("species", "").strip()
    name = data.get("name", "").strip()
    breed = data.get("breed", "").strip()
    age = data.get("age", "").strip()
    owner = data.get("owner", "").strip()
    severity = data.get("severity", "").strip()
    is_hospitalized = data.get("is_hospitalized", False)

    # Basic validations
    required_fields = {
        "species": species,
        "name": name,
        "breed": breed,
        "age": age,
        "owner": owner,
        "severity": severity
    }
    
    missing = [k for k, v in required_fields.items() if not v]
    if missing:
        view.render_error(
            handler, 
            400, 
            f"Os seguintes campos são obrigatórios e não podem estar vazios: {', '.join(missing)}"
        )
        return

    try:
        # Cast is_hospitalized explicitly to bool
        is_hosp_bool = bool(is_hospitalized)
        
        # Save to database using model
        pet_id = model.add_pet(
            species=species,
            name=name,
            breed=breed,
            age=age,
            owner=owner,
            severity=severity,
            is_hospitalized=is_hosp_bool
        )
        
        # Success response structure
        response_data = {
            "status": "success",
            "message": f"Pet '{name}' cadastrado com sucesso!",
            "data": {
                "id": pet_id,
                "species": species,
                "name": name,
                "breed": breed,
                "age": age,
                "owner": owner,
                "severity": severity,
                "is_hospitalized": is_hosp_bool
            }
        }
        view.render_json(handler, 201, response_data)
        
    except Exception as e:
        view.render_error(handler, 500, f"Erro ao salvar pet no banco de dados: {str(e)}")

def handle_list_pets(handler):
    """
    Retrieves the list of registered pets from the model and renders it as JSON.
    """
    try:
        pets_list = model.get_all_pets()
        view.render_json(handler, 200, pets_list)
    except Exception as e:
        view.render_error(handler, 500, f"Erro ao carregar pets: {str(e)}")
