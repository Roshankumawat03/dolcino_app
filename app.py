from flask import Flask, render_template, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dolcino-2024-app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dolcino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), default='default.jpg')
    prep_time = db.Column(db.String(20), default='30 min')
    servings = db.Column(db.String(20), default='4 servings')
    difficulty = db.Column(db.String(20), default='Medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Post {self.title}>'

# Routes
@app.route('/')
def index():
    featured_posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    return render_template('index.html', 
                         featured_posts=featured_posts, 
                         recent_posts=recent_posts[:3])

@app.route('/post/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('post.html', post=post)

@app.route('/api/posts')
def api_posts():
    posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'excerpt': p.excerpt,
        'category': p.category,
        'prep_time': p.prep_time,
        'servings': p.servings,
        'difficulty': p.difficulty,
        'image': p.image
    } for p in posts])

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    print(f"🔔 New subscriber: {email}")
    return jsonify({
        'success': True, 
        'message': 'Thank you for subscribing to Dolcino! 🎉'
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Initialize Database with IMAGES ✅
with app.app_context():
    db.create_all()
    
    if Post.query.count() == 0:
        posts = [
            {
                'title': 'Classic Tiramisu',
                'slug': 'classic-tiramisu',
                'excerpt': 'Authentic Italian tiramisu with mascarpone & coffee',
                'content': '''
                <h1>Classic Tiramisu Recipe</h1>
                <div class="recipe-content">
                    <div class="recipe-meta">
                        <h2>Ingredients</h2>
                        <div class="ingredients-grid">
                            <div class="ingredient-group">
                                <h3>For the Cream</h3>
                                <ul>
                                    <li>6 egg yolks</li>
                                    <li>¾ cup white sugar</li>
                                    <li>⅔ cup milk</li>
                                    <li>1¼ cups heavy cream</li>
                                    <li>1 pound mascarpone cheese</li>
                                </ul>
                            </div>
                            <div class="ingredient-group">
                                <h3>For Assembly</h3>
                                <ul>
                                    <li>1¼ cups strong brewed coffee</li>
                                    <li>4 tablespoons rum</li>
                                    <li>2 (7 ounce) packages ladyfinger cookies</li>
                                    <li>1 tablespoon unsweetened cocoa powder</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    
                    <div class="instructions">
                        <h2>Instructions</h2>
                        <ol class="instructions-list">
                            <li>Prepare the cream: Beat egg yolks in a large bowl with an electric mixer...</li>
                            <li>Beat heavy cream in a chilled glass or metal bowl...</li>
                            <li>Combine coffee and rum in a shallow bowl...</li>
                            <li>Cover and refrigerate for at least 4 hours...</li>
                        </ol>
                    </div>
                </div>
                ''',
                'category': 'Dessert',
                'image': 'tiramisu.jpg',
                'prep_time': '30 mins',
                'servings': '12 servings',
                'difficulty': 'Medium'
            },
            {
                'title': 'Truffle Risotto',
                'slug': 'truffle-risotto',
                'excerpt': 'Luxurious risotto with black truffles',
                'content': '<h1>Truffle Risotto</h1><p>Decadent Italian risotto with fresh black truffles. Creamy, rich, and indulgent...</p>',
                'category': 'Main Course',
                'image': 'risotto.jpg',
                'prep_time': '45 mins',
                'servings': '4 servings',
                'difficulty': 'Hard'
            },
            {
                'title': 'Avocado Toast',
                'slug': 'avocado-toast',
                'excerpt': 'Perfect brunch avocado toast',
                'content': '<h1>Avocado Toast</h1><p>Simple & delicious brunch classic with perfect seasoning...</p>',
                'category': 'Breakfast',
                'image': 'avocado-toast.jpg',
                'prep_time': '15 mins',
                'servings': '2 servings',
                'difficulty': 'Easy'
            }
        ]
        for post_data in posts:
            db.session.add(Post(**post_data))
        db.session.commit()
        print("✅ Database created with 3 recipes + images!")

if __name__ == '__main__':
    app.run(debug=True)