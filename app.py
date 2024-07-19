from flask import Flask, jsonify, request, render_template
import instaloader

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def get_profile():
    username = request.form['username']
    try:
        # Create an instance of Instaloader
        L = instaloader.Instaloader()

        # Load the profile
        profile = instaloader.Profile.from_username(L.context, username)

        # Get profile details
        profile_data = {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "number_of_posts": profile.mediacount,
            "followers": profile.followers,
            "following": profile.followees
        }
        posts = []
        for post in profile.get_posts():
            post_data = {
                "image_url": post.url, 
                "caption": post.caption,
                "likes": post.likes,
                "comments": post.comments
            }
            print(post.url)
            posts.append(post_data)
            # Limit the number of posts to prevent large responses
            if len(posts) >= 10:
                break

        return render_template('index.html', profile=profile_data, posts=posts)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
