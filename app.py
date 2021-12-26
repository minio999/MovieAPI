from movie import * 
import swagger

swagger()
Movie()

#running app
if __name__ == "__main__":
    Movie.app.run(debug=True)