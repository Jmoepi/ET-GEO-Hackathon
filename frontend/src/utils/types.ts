export interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  created_at: string;
}

export interface Vineyard {
  id: string;
  name: string;
  owner_id: string;
  location_lat: number | null;
  location_lon: number | null;
  boundary: string | null;
  area_hectares: number | null;
  created_at: string;
}

export interface Block {
  id: string;
  vineyard_id: string;
  name: string;
  cultivar: string | null;
  area_ha: number | null;
  geometry: string | null;
  planting_year: string | null;
  created_at: string;
}

export interface Observation {
  id: string;
  block_id: string;
  observation_date: string;
  eta: number | null;
  eto: number | null;
  kc: number | null;
  ndvi: number | null;
  soil_moisture: number | null;
  temperature: number | null;
  rainfall: number | null;
  phenology_stage: string | null;
  data_source: string | null;
  created_at: string;
}

export interface StressScore {
  id: string;
  block_id: string;
  stress_score: number;
  stress_category: string;
  confidence: number;
  model_version: string;
  contributors: FeatureContribution[];
  generated_at: string;
}

export interface FeatureContribution {
  metric: string;
  raw_value: number;
  normalised_value: number;
  weight: number;
  weighted_score: number;
  unit: string;
  available: boolean;
}

export interface Recommendation {
  id: string;
  block_id: string;
  recommendation_type: string;
  priority: string;
  status: string;
  explanation: string | null;
  confidence: number;
  generated_at: string;
}

export interface DecisionEvidence {
  id: string;
  recommendation_id: string;
  contributors_json: FeatureContribution[];
  stress_score: number;
  confidence: number;
  model_version: string;
  decision_rules_triggered: string[];
  explanation: string | null;
  generated_at: string;
}

export interface CopilotResponse {
  answer: string;
  decision_id: string | null;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
