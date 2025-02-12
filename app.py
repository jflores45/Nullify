from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def load_file(file_path):
        with open(file_path, 'r') as f:
            return f.read()
 # Load the test files
# followers_input = load_file("test1.txt")
# following_input = load_file("test2.txt")

def parse_user_data(text):
        lines = text.splitlines()
        users = []
        non_followees = []
        
        # Gather User Data
        Username = lines[1].strip()
        Post = lines[2].split()[0]
        Followers = lines[3].split()[0]
        Following = lines[4].split()[0]
        Name = lines[5].strip()

        skip_keywords = [
            "Change profile photo", f"{Username}'s profile picture", "Posts", "Saved", "Tagged", "Meta", "About", "Blog",
            "Jobs", "Help", "API", "Privacy", "Terms", "Locations", "Instagram Lite", "Following", "Followers", "Followed by",
            "Threads", "Search", "Meta Verified", "Contact Uploading", "Consumer Health Privacy",
            "English", "© 2024 Instagram from Meta"
        ]
       
        i = 7
        while i < len(lines):
            line = lines[i].strip()

            # Skip unwanted lines based on skip_keywords (e.g., Metadata)
            if any(keyword in line for keyword in skip_keywords):
                # print(f"{i} Skipped1: {line}")
                i += 1
                continue

            # 4-Line Block for Non-Followers: profile picture, username, ·, name (IGNORE)
            if i + 4 < len(lines) and "profile picture" in lines[i].lower() and lines[i + 2].strip() == "·" and ("Followed" in lines[i + 4] or "profile picture" in lines[i + 4].lower()):
                # print(f"{i} Skipped2: {line}")
                username = lines[i + 1].strip()
                name = lines[i + 3].strip()
                non_followees.append((username, name))
                i += 4  # Skip this non-follower block
                continue

            # 3-Line Block for Non-Followers Without a Name: profile picture, username, · (IGNORE)
            if i + 2 < len(lines) and "profile picture" in lines[i].lower() and lines[i + 2].strip() == "·" and "profile picture" in lines[i + 3].lower():
                # print(f"{i} Skipped3 not following: {line}")
                username = lines[i + 1].strip()
                non_followees.append((username, None))
                i += 3  # Skip this non-follower block
                continue

            # 2-Line Block for Followers: profile picture, username, name (No "·" at position i + 2)
            if i + 2 < len(lines) and "profile picture" in lines[i].lower() and "profile picture" not in lines[i + 2].strip():
                username = lines[i + 1].strip()
                name = lines[i + 2].strip()
                # print(f"{i} Success Following1: {username}, {name}")
                users.append((username, name))  # Add to users list
                i += 3  # Skip the entire 2-line block
                continue

            # 1-Line Block for Followers Without a Name: profile picture line should be skipped
            if i + 1 < len(lines) and "profile picture" in lines[i].lower() and "profile picture" in lines[i + 2].lower():
                username = lines[i + 1].strip()  # Name is in the next line
                # print(f"{i} Success Following2: {username}, {None}")
                users.append((username, None))  # Add to users list
                i += 2  # Skip the profile picture line and the username line
            
            # Empty lines
            if not line.strip():
                # print(f'{i} Empty')
                i += 1
                continue
        # print("Parsed Data:", users)
        # print('HERE', non_followees)
        return Username, Post, Followers, Following, Name, users, non_followees


@app.route('/find_unfollowers', methods=['POST'])
def find_unfollowers():
    followers_input = request.form['followers']
    following_input = request.form['following']

    if not following_input.strip() or not followers_input.strip():
        return render_template('result.html', error_message="Both lists must be filled out.")
    
    # Parse the inputs
    followers_data = parse_user_data(followers_input)
    following_data = parse_user_data(following_input)
   
    # Unpack the returned values
    username, post, followers, following, name, followers_users, non_followees = followers_data
    _, _, _, _, _, following_users, _ = following_data

    # If the data is a single comma-separated string
    followers_users = set(followers_users)
    following_users = set(following_users)

    # print("Following Users Set:", following_users)
    # print("Followers Users Set:", followers_users)

    # Find unfollowers people you follow but they don't follow you back
    unfollowers = following_users - followers_users
    print("Unfollowers:", unfollowers)

    # print("Unfollowers Set:", unfollowers)
    # Non-followees: people who follow you but you don't follow them back
    # print("Non-Followees Set:", non_followees)

    # print("Unfollowers:")
    # for user in unfollowers:
    #     print(f"Username: {user[0]}, Name: {user[1]}")

    # # print("\nNon-followees:")
    # for user in non_followees:
    #     print(f"Username: {user[0]}, Name: {user[1]}")

    num_unfollow = len(unfollowers)
    num_non_followees = len(non_followees)

    return render_template('result.html',
                           unfollowers=unfollowers, 
                           non_followees=non_followees,
                           username=username,
                           post=post,
                           followers=followers,
                           following=following,
                           name=name, num_unfollow=num_unfollow, num_non_followees=num_non_followees)


if __name__ == '__main__':
    app.run(debug=True)