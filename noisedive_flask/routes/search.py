import markdown
from noisedive_flask.helpers import (
    render_template,
    Blueprint,
    query,
    convert_row_and_apply_markdown
)

searchBlueprint = Blueprint("search", __name__)


@searchBlueprint.route("/search/<query_str>", methods=["GET", "POST"])
def search(query_str):
    queryNoWhiteSpace = query_str.replace("+", "")
    query_str = query_str.replace("+", " ")
    
    # Search for users
    queryUsers = query(
        "SELECT * FROM users WHERE userName LIKE ? OR userName LIKE ?",
        params=(f"%{query_str}%", f"%{queryNoWhiteSpace}%"),
        fetchone=False
    )
    
    # Search for posts
    queryTags = query(
        "SELECT * FROM posts WHERE tags LIKE ? OR tags LIKE ?",
        params=(f"%{query_str}%", f"%{queryNoWhiteSpace}%"),
        fetchone=False
    )
    queryTitles = query(
        "SELECT * FROM posts WHERE title LIKE ? OR title LIKE ?",
        params=(f"%{query_str}%", f"%{queryNoWhiteSpace}%"),
        fetchone=False
    )
    queryAuthors = query(
        "SELECT * FROM posts WHERE author LIKE ? OR author LIKE ?",
        params=(f"%{query_str}%", f"%{queryNoWhiteSpace}%"),
        fetchone=False
    )
    
    posts = queryTags + queryTitles + queryAuthors
    
    # Remove duplicates from the posts list based on the 'id' column
    seen_ids = set()
    posts = [post for post in posts if not (post.id in seen_ids or seen_ids.add(post.id))]
    # posts = convert_row_and_apply_markdown(posts)
    
    for post in posts:
        print(post.id)
        if post.id==14:
            print(post.content)
    # import pdb; pdb.set_trace()

    return render_template(
        "search.html",
        posts=posts,
        users=queryUsers,
        query=query_str,
        empty= not (posts or queryUsers),
    )