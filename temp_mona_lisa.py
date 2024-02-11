from PIL import Image, ImageDraw, ImageChops
import numpy as np
import pandas as pd
import copy
import matplotlib.pyplot as plt

polygons = [{'vertices': [(179, 203), (162, 80), (110, 108)], 'RGBA': (0, 0, 255, 125)},
{'vertices': [(239, 65), (216, 179), (11, 79)], 'RGBA': (0, 255, 0, 125)},
{'vertices': [(209, 123), (23, 245), (194, 187)], 'RGBA': (255, 0, 0, 125)}]

def draw(polygons, size):
    """ Draws the collection of polygons in a canvas. """
    
    # Draw the canvas in white
    img = Image.new('RGB', (size[0], size[1]), (255, 255, 255))
    drw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw each polygon
    for pol in polygons:
        drw.polygon(pol["vertices"], pol["RGBA"])
    
    return(img.convert("RGB"))



def random_triangles(N, size, colour="random", alpha="random"):
    """ Generates a population of random triangles. """
    
    collection = []
    
    for i in range(N):
        # Generate vertex coordinates
        coords = [ (np.random.randint(0, size[0]), np.random.randint(0, size[1])) for i in range(3)]
        
        # Generate alpha
        if alpha == "random":
            a = np.random.randint(0, 256)
        else:
            a = alpha

        # Generate colour
        if colour == "white":
            rgba = (255,255,255,a)
        elif colour == "black":
            rgba = (0, 0, 0, a)
        elif colour == "random":
            rgba = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256), a)

        triangle = {"vertices": coords, "RGBA": rgba}
        collection.append(triangle)
        
    return(collection)

# Generate a collection of random triangles
# N, M = 728, 546
# collection = random_triangles(N=50, size=(N,M), colour="random", alpha="random")
# # Draw the triangles
# img = draw(collection, size=(N,M))
# img.show()

# Read image
image_path = "mona_lisa_v2.png"
# Open the image and convert it to RGB (no alpha channel)
target = Image.open(image_path).convert("RGB")
# target.show()


# diff = ImageChops.difference(img, target)

# Compute pixel difference
def pixel_difference(candidate,target):
    """ Computes the image difference pixel by pixel"""
    diff = ImageChops.difference(candidate, target)
    totdiff = np.array(diff.getdata()).sum()
    return(totdiff)

# diff = pixel_difference(img,target)
# print(diff)

# Compute maximum pixel difference
def max_pixel_difference(target):
    """ Computes the maximum pixel difference from white canvas"""
    white = Image.new('RGB', target.size, (255, 255, 255))
    diff = ImageChops.difference(white, target)
    maxdiff = np.array(diff.getdata()).sum()
    return(maxdiff)

# maxdiff = max_pixel_difference(target)
# fitness = (1 - diff / maxdiff) * 100
# print("Fitness = " + str(np.round(fitness,4)) + "%")

def mutation(original, size, mtype="hard"):
    """
    Produces a mutation within a collection.
    
    The mutation can be "Soft", "Medium", "Hard" or as described in this page
    (https://alteredqualia.com/visualization/evolve/)
    """
    # Produce a deep copy instead of modifying the original
    mutant = copy.deepcopy(original)
    
    # Randomly selecting the index of polygon to mutate
    polidx = np.random.randint(len(mutant))
    
    if mtype == "soft":
        # Implementing soft mutation is part of the exercise 2
        pass
    elif mtype == "medium":
        # Implementing medium mutation is part of the exercise 2
        pass
    elif mtype == "hard":
        # Randomly change the color and transparency
        mutant[polidx]["RGBA"] = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        
        # Replace one of the vertex or random values
        vtidx = np.random.randint(len(mutant[polidx]["vertices"]))
        mutant[polidx]["vertices"][vtidx] = (np.random.randint(0, size[0]), np.random.randint(0, size[1]))
        
    else:
        # Raise an error if non of the above
        raise ValueError("Wrong value for mtype")
    
    return(mutant)

# Create a collection of black semi-transparent triangles
collection = random_triangles(N=3, size=(200,200), colour="black", alpha=100)
# Render the initial collection
original_img = draw(collection, size=(200,200))
# Mutate the original collection
new_collection = mutation(collection, size=(200,200), mtype="hard")
# Render the new mutant image
mutated_img = draw(new_collection, size=(200,200))

# Plot the original and mutated images side by side
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7,3))
ax[0].imshow(original_img);
ax[0].set_title("Original")
ax[0].axis('off')
ax[1].imshow(mutated_img);
ax[1].set_title("Mutated")
ax[1].axis('off')   


def triangle_painting_hill_climbing(target, Ntri=100, maxit=10001, mtype="hard", colour_init="black", alpha_init=100, logs=True, every=500, outdir="output_images"):
    """
    Runs the Hill Climbing algorithm to reproduce the target picture using triangles.
    """
    
    size = target.size
    # Compute maximum pixel difference for this target 
    maxdiff = max_pixel_difference(target)
    
    # Generate an initial candidate 
    best = random_triangles(Ntri, size=size, colour=colour_init, alpha=alpha_init)
    best_img = draw(best, size=size)
    # Pixel difference between candidate and target
    diff = pixel_difference(best_img,target)
    fitness = (1 - diff / maxdiff) * 100
    
    improvements = 0
    
    info = []
    
    for i in range(maxit):
        # store information every x rounds
        if i%every == 0:
            # Print in screen
            if logs==True:
                print("Mutations: " + str(i) + " Improvements: " + str(improvements) + " Fitness: " + str(np.round(fitness,2)) + "%")
            # Save image
            best_img = draw(best, size=size)
            outpath = outdir +  str(i) + ".png"
            best_img.save(outpath)
            # output variables
            info.append([i, improvements, fitness, outpath])
            
        # Mutate the best candidate
        new = mutation(best, size=size, mtype=mtype)
        # Generate a new image
        new_img = draw(new, size=size)
        # Compute the difference
        newdiff = pixel_difference(new_img,target)
        
        if newdiff < diff:
            # If the new is better update the candidate features
            diff = newdiff
            best = copy.deepcopy(new)
            improvements += 1
            fitness = (1 - diff / maxdiff) * 100

    dfout = pd.DataFrame(info, columns=["mutations","improvements","fitness","image path"])
    
    return(dfout)

df = triangle_painting_hill_climbing(target, Ntri=50, maxit=100001, every=1000, mtype="hard", outdir="output_images")