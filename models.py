from extensions import db
from sqlalchemy.orm import validates

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

   
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "super_name": self.super_name,
            "hero_powers": [hp.to_dict() for hp in self.hero_powers]  # Include hero powers in response
        }

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    
    @validates('description')
    def validate_description(self, key, description):
        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

   
    power = db.relationship('Power')

   
    @validates('strength')
    def validate_strength(self, key, strength):
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return strength

    def to_dict(self):
        return {
            "id": self.id,
            "hero_id": self.hero_id,
            "power_id": self.power_id,
            "strength": self.strength,
            "power": self.power.to_dict()
        }