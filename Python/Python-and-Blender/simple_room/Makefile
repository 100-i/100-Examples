BLENDER_USER_SCRIPTS=src/simple_room

BLENDER_BACKGROUND_OPTS=--background

BLENDER_AUTOEXEC=--enable-autoexec

BLENDER_DEBUG_OPTS=--debug-all

ANIMATION_FILES=src/simple_room

all: test_all

test_all : $(BLENDER_USER_SCRIPTS)/set.py
	blender $(BLENDER_AUTOEXEC) --python $^

person : $(BLENDER_USER_SCRIPTS)/person.py
	blender $(BLENDER_AUTOEXEC) --python $^

room : $(BLENDER_USER_SCRIPTS)/room.py
	blender $(BLENDER_AUTOEXEC) --python $^

python : $(BLENDER_USER_SCRIPTS)/test.py
	blender $(BLENDER_BACKGROUND_OPTS) --python $^

python-gui : $(BLENDER_USER_SCRIPTS)/test.py
	blender $(BLENDER_AUTOEXEC) --python $^ 

animation : $(ANIMATION FILES)/test.py
	blender $(BLENCER_OPTS) --ptyhon $^ --render-anim

$(BLENDER_USER_SCRIPTS)/test.py:

.PHONY: all
