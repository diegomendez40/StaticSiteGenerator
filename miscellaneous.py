original_text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
splitted = original_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
print(splitted)