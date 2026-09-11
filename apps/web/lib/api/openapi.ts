export interface paths {
  "/v1/study/sessions": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Create Session */
    post: operations["create_session_v1_study_sessions_post"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** Get Session */
    get: operations["get_session_v1_study_sessions__session_id__get"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/current-trial": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** Get Current Trial */
    get: operations["get_current_trial_v1_study_sessions__session_id__current_trial_get"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/trial-attempts": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Create Trial Attempt */
    post: operations["create_trial_attempt_v1_study_sessions__session_id__trial_attempts_post"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/responses": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Submit Response */
    post: operations["submit_response_v1_study_sessions__session_id__responses_post"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/questionnaire": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** Get Questionnaire */
    get: operations["get_questionnaire_v1_study_sessions__session_id__questionnaire_get"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/post-study": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Submit Questionnaire */
    post: operations["submit_questionnaire_v1_study_sessions__session_id__post_study_post"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/stop": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    get?: never;
    put?: never;
    /** Stop Session */
    post: operations["stop_session_v1_study_sessions__session_id__stop_post"];
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/study/sessions/{session_id}/debrief": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /** Get Debrief */
    get: operations["get_debrief_v1_study_sessions__session_id__debrief_get"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/health": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /**
     * Health Check
     * @description Return a lightweight liveness response for local development.
     */
    get: operations["health_check_health_get"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
  "/v1/project-status": {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    /**
     * Project Status
     * @description Return non-sensitive public project metadata.
     */
    get: operations["project_status_v1_project_status_get"];
    put?: never;
    post?: never;
    delete?: never;
    options?: never;
    head?: never;
    patch?: never;
    trace?: never;
  };
}
export type webhooks = Record<string, never>;
export interface components {
  schemas: {
    /** AssistanceView */
    AssistanceView: {
      /** Recommendation Option Id */
      recommendation_option_id: string;
      /** Recommendation Name */
      recommendation_name: string;
      /** Explanation */
      explanation?: string | null;
      /** Confidence Percent */
      confidence_percent?: number | null;
    };
    /** ConsentRequest */
    ConsentRequest: {
      /**
       * Consent
       * @constant
       */
      consent: true;
    };
    /** DebriefView */
    DebriefView: {
      /** Title */
      title: string;
      /** Paragraphs */
      paragraphs: string[];
    };
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components["schemas"]["ValidationError"][];
    };
    /** OptionView */
    OptionView: {
      /** Id */
      id: string;
      /** Name */
      name: string;
      /** Attributes */
      attributes: {
        [key: string]: string;
      };
    };
    /** ProjectStatus */
    ProjectStatus: {
      /** Name */
      name: string;
      /** Phase */
      phase: string;
      /** Message */
      message: string;
    };
    /** QuestionnaireItem */
    QuestionnaireItem: {
      /** Id */
      id: string;
      /** Statement */
      statement: string;
    };
    /** QuestionnaireRequest */
    QuestionnaireRequest: {
      /** Responses */
      responses: {
        [key: string]: number;
      };
      /** Free Text */
      free_text?: string | null;
    };
    /** QuestionnaireView */
    QuestionnaireView: {
      /** Items */
      items: components["schemas"]["QuestionnaireItem"][];
      /** Scale */
      scale: {
        [key: string]: string;
      };
      /** Free Text Prompt */
      free_text_prompt: string;
    };
    /** SessionCreated */
    SessionCreated: {
      /** Session Id */
      session_id: string;
      /** Anonymous Participant Id */
      anonymous_participant_id: string;
      status: components["schemas"]["SessionStatus"];
      /** Study Version */
      study_version: string;
    };
    /** SessionProgress */
    SessionProgress: {
      /** Session Id */
      session_id: string;
      status: components["schemas"]["SessionStatus"];
      /** Current Trial Index */
      current_trial_index: number;
      /** Total Trials */
      total_trials: number;
      /** Study Version */
      study_version: string;
      /**
       * Started At
       * Format: date-time
       */
      started_at: string;
      /** Completed At */
      completed_at?: string | null;
    };
    /**
     * SessionStatus
     * @enum {string}
     */
    SessionStatus: "IN_PROGRESS" | "QUESTIONNAIRE_PENDING" | "COMPLETED" | "STOPPED";
    /** TrialAttemptCreated */
    TrialAttemptCreated: {
      /** Attempt Id */
      attempt_id: string;
      /** Trial Id */
      trial_id: string;
      /** Attempt Number */
      attempt_number: number;
    };
    /** TrialAttemptRequest */
    TrialAttemptRequest: {
      /** Trial Id */
      trial_id: string;
    };
    /** TrialResponseReceipt */
    TrialResponseReceipt: {
      /** Trial Id */
      trial_id: string;
      next_status: components["schemas"]["SessionStatus"];
      /** Next Trial Index */
      next_trial_index: number;
      /** Total Trials */
      total_trials: number;
    };
    /** TrialResponseRequest */
    TrialResponseRequest: {
      /** Trial Id */
      trial_id: string;
      /** Attempt Id */
      attempt_id: string;
      /** Selected Option Id */
      selected_option_id: string;
      /** Participant Confidence */
      participant_confidence: number;
      /** Reasoning */
      reasoning?: string | null;
      /** Response Time Ms */
      response_time_ms: number;
      /** Idempotency Key */
      idempotency_key: string;
    };
    /** TrialView */
    TrialView: {
      /** Id */
      id: string;
      /** Title */
      title: string;
      /** Context */
      context: string;
      /** Decision Question */
      decision_question: string;
      /** Criteria */
      criteria: string;
      /** Attribute Labels */
      attribute_labels: string[];
      /** Options */
      options: components["schemas"]["OptionView"][];
      assistance?: components["schemas"]["AssistanceView"] | null;
      /** Trial Number */
      trial_number: number;
      /** Total Trials */
      total_trials: number;
    };
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (string | number)[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
  create_session_v1_study_sessions_post: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["ConsentRequest"];
      };
    };
    responses: {
      /** @description Successful Response */
      201: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["SessionCreated"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  get_session_v1_study_sessions__session_id__get: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["SessionProgress"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  get_current_trial_v1_study_sessions__session_id__current_trial_get: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["TrialView"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  create_trial_attempt_v1_study_sessions__session_id__trial_attempts_post: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["TrialAttemptRequest"];
      };
    };
    responses: {
      /** @description Successful Response */
      201: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["TrialAttemptCreated"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  submit_response_v1_study_sessions__session_id__responses_post: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["TrialResponseRequest"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["TrialResponseReceipt"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  get_questionnaire_v1_study_sessions__session_id__questionnaire_get: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["QuestionnaireView"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  submit_questionnaire_v1_study_sessions__session_id__post_study_post: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["QuestionnaireRequest"];
      };
    };
    responses: {
      /** @description Successful Response */
      204: {
        headers: {
          [name: string]: unknown;
        };
        content?: never;
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  stop_session_v1_study_sessions__session_id__stop_post: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      204: {
        headers: {
          [name: string]: unknown;
        };
        content?: never;
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  get_debrief_v1_study_sessions__session_id__debrief_get: {
    parameters: {
      query?: never;
      header?: never;
      path: {
        session_id: string;
      };
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["DebriefView"];
        };
      };
      /** @description Validation Error */
      422: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  health_check_health_get: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": {
            [key: string]: string;
          };
        };
      };
    };
  };
  project_status_v1_project_status_get: {
    parameters: {
      query?: never;
      header?: never;
      path?: never;
      cookie?: never;
    };
    requestBody?: never;
    responses: {
      /** @description Successful Response */
      200: {
        headers: {
          [name: string]: unknown;
        };
        content: {
          "application/json": components["schemas"]["ProjectStatus"];
        };
      };
    };
  };
}
