/*
*
* */
workflow = {
    /*
    *
    * Workflow object must be:
    * {
    *   stage_id: {
    *       next: function() {
    *           // This method calculated id for next stage
    *           return ''
    *       },
    *       stay: function() {
    *           // This method fires when next() returned same stage id as current stage id
    *       },
    *       rollback: function(){
    *           // This method fires when passed stages must be rolled back
    *       },
    *       load(workflow_object){
    *           // This method fires before current stage is changed
    *       },
    *       init: function(workflow_object){
    *           // This method fires after current stage is changed
    *       }
    *   }
    * }
    * */
    stages: null,

    passed_stages: [],

    curr_stage_id: '',

    /*
    *
    * */
    workflow_finished: function(workflow_obj){
        console.log('Workflow finished');
    },

    /*
    *
    * */
    init: function(workflow_stages, initial_stage_id){
        this.stages = workflow_stages;
        this.passed_stages = [];
        this.curr_stage_id = '';
        this.change_stage(initial_stage_id);
    },

    /*
    * Change stage, rollback if necessary
    * */
    change_stage: function(stage_id){
        var target_stage = this.stages[stage_id];

        // Loading
        if(target_stage.hasOwnProperty('load')){
            target_stage.load(this);
        }

        // Set new current stage id
        this.curr_stage_id = stage_id;

        // Initialization
        if(target_stage.hasOwnProperty('init')){
            target_stage.init(this)
        }
    },

    /*
    * Performs change current stage to next stage, determined with next() function of current one
    * */
    next_stage: function(){
        var next_stage_id = this.stages[this.curr_stage_id].hasOwnProperty('next') ?
            this.stages[this.curr_stage_id].next() : null;

        if(next_stage_id && next_stage_id != this.curr_stage_id) {
            var prev_stage = this.curr_stage_id;
            this.passed_stages.push(prev_stage);
            this.change_stage(next_stage_id);
            return true;
        } else if (next_stage_id && next_stage_id == this.curr_stage_id) {
            if(this.stages[this.curr_stage_id].hasOwnProperty('stay')){
                this.stages[this.curr_stage_id].stay();
            }
            return false;
        } else if (next_stage_id === false) {
            return false;
        } else if (next_stage_id === null) {
            this.workflow_finished(this);
            return false;
        }
    },

    /*
    * Rolls back up to stage with id {stage_id}
    * */
    rollback_stage: function(stage_id) {
        if (this.passed_stages.indexOf(stage_id) >= 0) {
            var last_stage_id = this.curr_stage_id;
            while (last_stage_id != stage_id) {
                var last_stage = this.stages[last_stage_id];
                if (last_stage.hasOwnProperty('rollback')) last_stage.rollback();
                last_stage_id = this.passed_stages.pop();
            }
            last_stage = this.stages[last_stage_id];
            if (last_stage.hasOwnProperty('rollback')) last_stage.rollback();
            this.change_stage(stage_id);
            return true;
        } else {
            return false;
        }
    }
};
