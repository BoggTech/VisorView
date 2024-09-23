// default resource/model paths
model-path $MAIN_DIR
model-path $THIS_PRC_DIR/resources

// uncomment to disable model caching
model-cache-dir

// anti-aliasing
framebuffer-multisample 1
multisamples 8

egg-object-type-shadow          <Scalar> bin { shadow } <Scalar> alpha { blend-no-occlude }
cull-bin shadow 15 unsorted

egg-object-type-ground          <Scalar> bin { ground }
egg-object-type-shadow-ground   <Scalar> bin { ground }
cull-bin ground 14 unsorted

// uncomment to enable framerate meter
//show-frame-rate-meter #t

// uncomment to enable limited fps, where clock-frame-rate is the desired framerate
//clock-mode limited
//clock-frame-rate 5