from flask import request, jsonify
from app import app, db
from models import Hero, Power, HeroPower


@app.route('/')
def index():
    return "Phase 4 Code Challenge: Superheroes!"
# Route: GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    """Return a list of all heroes with id, name, and super_name."""
    heroes = Hero.query.all()
    return jsonify([
        {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
        for hero in heroes
    ])

# Route: GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    """Return details of a specific hero by ID, including their powers."""
    hero = Hero.query.get(id)

    if hero:
        # Format the hero powers in the specified format
        hero_powers = [
            {
                "hero_id": hp.hero_id,
                "id": hp.id,
                "power": {
                    "id": hp.power.id,
                    "name": hp.power.name,
                    "description": hp.power.description
                },
                "power_id": hp.power_id,
                "strength": hp.strength
            }
            for hp in hero.hero_powers
        ]
        return jsonify({
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": hero_powers
        })

    return jsonify({"error": "Hero not found"}), 404

# Route: GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    """Return a list of all powers."""
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

# Route: GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    """Return details of a specific power by ID."""
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    return jsonify({"error": "Power not found"}), 404

# Route: PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    """Update an existing Power."""
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.json
    description = data.get('description')

    # Validation
    if not description:
        return jsonify({"errors": ["description field is required"]}), 400

    # Attempt to update the description with validation
    try:
        power.description = description
        db.session.commit()
    except Exception:
        db.session.rollback()  # Rollback if an error occurs
        return jsonify({"errors": ["validation errors"]}), 400

    # Return the updated power in the specified format
    return jsonify({
        "description": power.description,
        "id": power.id,
        "name": power.name
    }), 200

# Route: POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    """Create a new HeroPower association."""
    data = request.json
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    # Validation
    if not strength or not power_id or not hero_id:
        return jsonify({"errors": ["strength, power_id, and hero_id fields are required"]}), 400

    # Check if hero and power exist
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 404

    # Create and save the new HeroPower
    hero_power = HeroPower(strength=strength, hero_id=hero_id, power_id=power_id)
    db.session.add(hero_power)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()  # Rollback if an error occurs
        return jsonify({"errors": ["validation errors"]}), 400

    return jsonify({
        "id": hero_power.id,
        "hero_id": hero_power.hero_id,
        "power_id": hero_power.power_id,
        "strength": hero_power.strength,
        "hero": {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        },
        "power": {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    }), 201