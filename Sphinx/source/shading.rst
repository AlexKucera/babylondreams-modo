Shading
=======

Fix Orphans
-----------

Finds any Shader Tree items that have become unparented and parents them back to the Shader Tree.

Collect all TextureLocators
-----------------------

Modo used to have this built in. Now it's back. Call the command and every Texture Locator in the scene will get put into a top level folder caller textureLocator_group. Keeps your scene nice and clena even if you have imported tons of individual scenes and have Texture Locators all over the Item list.

I use this to not accidentally delete any Texture Locators when deleting entire Item list hierarchies.

Create Per Material RenderOutputs
---------------------------------

Adds an Alpha and/or a Final Color output to any selected Material Group. The outputs will be named with the name of the Material Group plus the output type, e.g.: red_metal_alpha.

Rename V-Ray Proxies based on Proxy Filename
--------------------------------------------

As the name implies. Click the button and modo will go through your scene, find any V-Ray Proxies, look at the vrmesh file and rename the item to the name of the vrmesh.

Texture Effects Chooser
-----------------------

The top dropdown defines your filter words, the words modo looks for in your texture's file name. You can input anything you need into the text field.
By default it uses a predefined set of filter words and you can also choose only a subset of those filter words.

The bottom dropdown allows you to choose which channel effect you want to apply to the textures.

There are three options:

1. Use Default Channel Types. This only works in combination with one of the predefined filter sets and will pick the appropriate channel effect. So diff, will get Diffuse Color as channel effect, etc.
2. Use modo Command Dialog will show the default modo dialog that you also get when manually selecting a channel effect. This has the benefit that everything is sorted and can be found where you expect it.
3. A flat list of all channel effects. If you know what you are looking for this is the fastest way. Just type in the name in the search field at that top.

If you leave the default selection of base_all and base_types and hit ok, it will go through all image textures in the shader tree and assign them to the appropriate channel effect.

Blend Hierarchy
---------------

The command creates an easily animateable setup to dissolve/fade a hierarchy of items. By selecting the parent item and running the command a few things happen:

    1. A group with the whole item hierarchy gets created
    2. A shader setup gets created and put at the top of the shader tree
    3. The shader setup gets linked to the group

To animate the blend/dissolve you open the corresponding Shader group and animate the constant's value.

Blend Arbitrary
---------------

Same as Blend Hierarchy, but allows blending of completely unrelated items in the scene.

BBox Instance Toggle
--------------------

Toggles the bounding box display of all instances of a given selection (or all instances in the scene if nothing is selected).