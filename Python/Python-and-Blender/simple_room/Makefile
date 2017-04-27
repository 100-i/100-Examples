BLENDER_USER_SCRIPTS=src/simple_room

BLENDER_OPTS="--background"

BLENDER_AUTOEXEC="--enable-autoexec"

BLENDER_DEBUG_OPTS="--debug-all"

ANIMATION_FILES=src/simple_room

all: python

python : $(BLENDER_USER_SCRIPTS)/test.py
	blender $(BLENDER_OPTS) --python $^

python-gui : $(BLENDER_USER_SCRIPTS)/test.py
	blender $(BLENDER_AUTOEXEC) --python $^ 

animation : $(ANIMATION FILES)/test.py
	blender $(BLENCER_OPTS) --ptyhon $^ --render-anim

$(BLENDER_USER_SCRIPTS)/test.py:

.PHONY: all
