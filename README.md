# Smart-Health-Mirror: Mirror-Module

The mirror is the GUI of the [Smart Health Mirror framework](https://github.com/JohannaLatt/Master-Thesis-Smart-Health-Mirror). It is built using the [kivy](https://kivy.org/)-framework to optimize for 2D-/3D-graphical rendering especially relevant for rendering the skeleton, but also for rendering dynamic text and graphs. The mirror only sends a message on startup to notify the server that it is ready. After that, it only receives data from the server. Currently, the mirror supports multiple operations that simplify communication between server-modules and the mirror:

* **Show Text**: The mirror can show text either statically at a certain position of the screen (and with a certain alignment, font-size and -color etc.) or dynamically following a user's joint over time. The text can also be faded in and out and it can be specified for how long the text stays.
* **Clear skeleton**: Clears the rendering of the skeleton off the screen. Used when tracking is lost.
* **Render skeleton**: Accepts the preprocessed skeleton format described under [server](#Server) and renders an OpenGL 2D skeleton on the screen. The skeleton is always positioned at the bottom of the screen to account for the assumption that the prototype is run on a full-room height mirror/screen, i.e. the rendered skeleton should 'stand' at the bottom of the screen. 
* **Change skeleton color**: Takes the name of a joint or a bone and changes the color of it respectively.
* **Update graphs**: Takes three values and displays them on the three graphs on the GUI, assuming the values are x-, y- and z-coordinates of a joint.

## Installation

The mirror is a kivy appliation that is run as a normal python application:

1. Make sure to have the necessary requirements installed: `pip install -r [link to requirements.txt in Mirror folder]` (if you use virtual environments, make sure to activate it)
  * For garden (used for the graphs) an additional requirement has to be manually installed: `garden install --upgrade graph`
2. Go to /Mirror in this repository: `cd Mirror`
4. Update the RabbitMQ-messaging-server-ip in the [config-file](https://github.com/JohannaLatt/Smart-Health-Mirror/blob/master/Mirror/config/mirror_config.ini) if needed
5. Run the application
```
python index.py
```
