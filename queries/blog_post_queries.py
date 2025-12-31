from models.blog_post import BlogPost
from models.result import ResultMessage
from extensions import db


class BlogPostQueries:

    def get_all_posts(self):
        try:

            print("===================> Getting all posts")

            all_posts = BlogPost.query.all()

            if len(all_posts) == 0:
                result = ResultMessage(all_posts, "info", "No posts found", 404)
                print(result.message)
                print("===================> Finished getting all posts")
                return result

            else:
                result = ResultMessage(all_posts, "success", "All posts found", 200)
                print(result.message)
                print("===================> Finished getting all posts")
                return result


        except Exception as e:
            result = ResultMessage("", "error", f"Error getting all posts: {e}", 500)
            print(result.message)
            return result


    def get_post_by_id(self, post_id):
        try:

            print("===================> Getting post by id")

            post = BlogPost.query.filter_by(id=post_id).all()

            if len(post) == 0:
                result = ResultMessage(post_id, "info", f"No post found by that id {post_id}", 404)
                print(result.message)
                print("====================> Finished getting post by id")
                return result

            else:
                result = ResultMessage(post, "success", f"Post with id {post_id} found", 200)
                print(result.message)
                print("====================> Finished getting post by id")
                return result

        except Exception as e:
            result = ResultMessage("", "error", f"Error getting post by id: {e}", 500)
            print(result.message)
            return result


    def add_new_post(self, new_post):
        try:
            print("===================> Adding new post")

            db.session.add(new_post)
            db.session.commit()

            print("====================> Finished adding new post")

            result = ResultMessage(new_post, "success", f"New post {new_post} added successfully", 200)
            print(result.message)
            return result

        except Exception as e:
            result = ResultMessage("", "error", f"Error adding new post: {e}", 500)
            print(result.message)
            return result


    def update_post(self, edited_post, requested_post):

        try:
            print("====================> Updating post")
            requested_post.title = edited_post.title
            requested_post.subtitle = edited_post.subtitle
            requested_post.author = edited_post.author
            requested_post.body = edited_post.body
            requested_post.img_url = edited_post.img_url

            db.session.add(requested_post)
            db.session.commit()

            print("====================> Finished updating post")

            result = ResultMessage("", "success", f"Post {requested_post.title} updated successfully", 200)
            print(result.message)
            return result


        except Exception as e:
            result = ResultMessage("", "error", f"Error updating post: {e}", 500)
            print(result.message)
            return result

    def delete_post(self, post_id):
        try:
            print("====================> Deleting post")

            post_to_be_deleted = self.get_post_by_id(post_id).data[0]

            db.session.delete(post_to_be_deleted)
            db.session.commit()

            print("====================> Finished deleting post")

            result = ResultMessage("", "success", f"Post {post_id} deleted successfully", 200)
            print(result.message)
            return result

        except Exception as e:
            result = ResultMessage("", "error", f"Error deleting post: {e}", 500)
            print(result.message)
            return result
