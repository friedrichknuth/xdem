"""
Terrain attributes
==================

Terrain attributes generated from a DEM have a multitude of uses for analytic and visual purposes.
Here is an example of how to generate these products.

For more information, see the :ref:`terrain_attributes` chapter and the
:ref:`sphx_glr_auto_examples_plot_slope_methods.py` example.
"""
# sphinx_gallery_thumbnail_number = 12
import matplotlib.pyplot as plt

import xdem

# %%
# **Example data**

dem = xdem.DEM(xdem.examples.get_path("longyearbyen_ref_dem"))


def plot_attribute(attribute, cmap, label=None, vlim=None):
    plt.figure(figsize=(8, 5))

    if vlim is not None:
        if isinstance(vlim, (int, float)):
            vlims = {"vmin": -vlim, "vmax": vlim}
        elif len(vlim) == 2:
            vlims = {"vmin": vlim[0], "vmax": vlim[1]}
    else:
        vlims = {}

    plt.imshow(
        attribute.squeeze(),
        cmap=cmap,
        extent=[dem.bounds.left, dem.bounds.right, dem.bounds.bottom, dem.bounds.top],
        **vlims
    )
    if label is not None:
        cbar = plt.colorbar()
        cbar.set_label(label)

    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()

    plt.show()


# %%
# Slope
# -----

slope = xdem.terrain.slope(dem.data, resolution=dem.res)

plot_attribute(slope, "Reds", "Slope (°)")

# %%
# Aspect
# ------

aspect = xdem.terrain.aspect(dem.data)

plot_attribute(aspect, "twilight", "Aspect (°)")

# %%
# Hillshade
# ---------

hillshade = xdem.terrain.hillshade(dem.data, resolution=dem.res, azimuth=315.0, altitude=45.0)

plot_attribute(hillshade, "Greys_r")

# %%
# Curvature
# ---------

curvature = xdem.terrain.curvature(dem.data, resolution=dem.res)

plot_attribute(curvature, "RdGy_r", "Curvature (100 / m)", vlim=1)

# %%
# Planform curvature
# ------------------

planform_curvature = xdem.terrain.planform_curvature(dem.data, resolution=dem.res)

plot_attribute(planform_curvature, "RdGy_r", "Planform curvature (100 / m)", vlim=1)

# %%
# Profile curvature
# -----------------
profile_curvature = xdem.terrain.profile_curvature(dem.data, resolution=dem.res)

plot_attribute(profile_curvature, "RdGy_r", "Profile curvature (100 / m)", vlim=1)

# %%
# Topographic Position Index
# --------------------------
tpi = xdem.terrain.topographic_position_index(dem.data)

plot_attribute(tpi, "Spectral", "Topographic Position Index", vlim=5)

# %%
# Terrain Ruggedness Index
# ------------------------
tri = xdem.terrain.terrain_ruggedness_index(dem.data)

plot_attribute(tri, "Purples", "Terrain Ruggedness Index")

# %%
# Roughness
# ---------
roughness = xdem.terrain.roughness(dem.data)

plot_attribute(roughness, "Oranges", "Roughness")

# %%
# Rugosity
# --------
rugosity = xdem.terrain.rugosity(dem.data, resolution=dem.res)

plot_attribute(rugosity, "YlOrRd", "Rugosity")

# %%
# Fractal roughness
# -----------------
fractal_roughness = xdem.terrain.fractal_roughness(dem.data)

plot_attribute(fractal_roughness, "Reds", "Fractal roughness")

# %%
# Generating multiple attributes at once
# --------------------------------------

attributes = xdem.terrain.get_terrain_attribute(
    dem.data,
    attribute=["hillshade", "slope", "aspect", "curvature", "terrain_ruggedness_index", "rugosity"],
    resolution=dem.res
)

plt.figure(figsize=(8, 6.5))

plt_extent=[dem.bounds.left, dem.bounds.right, dem.bounds.bottom, dem.bounds.top]

cmaps = ["Greys_r", "Reds", "twilight", "RdGy_r", "Purples", "YlOrRd"]
labels = ["Hillshade", "Slope (°)", "Aspect (°)", "Curvature (100 / m)", "Terrain Ruggedness Index", "Rugosity"]
vlims = [(None, None) for i in range(6)]
vlims[3] = [-2, 2]

for i in range(6):
    plt.subplot(3, 2, i+1)
    plt.imshow(attributes[i].squeeze(), cmap=cmaps[i], extent=plt_extent, vmin=vlims[i][0], vmax=vlims[i][1])
    cbar = plt.colorbar()
    cbar.set_label(labels[i])
    plt.xticks([])
    plt.yticks([])

plt.tight_layout()
plt.show()