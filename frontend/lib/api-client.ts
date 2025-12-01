// API Client for FastAPI Backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface APIResponse<T> {
  data?: T;
  error?: string;
}

// Generic fetch wrapper
async function apiFetch<T>(endpoint: string, options?: RequestInit): Promise<APIResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    console.error("API Fetch Error:", error);
    return { error: error instanceof Error ? error.message : "Unknown error" };
  }
}

// Seasons API
export const seasonsApi = {
  getAll: () => apiFetch<Season[]>("/seasons"),
  getByYear: (year: number) => apiFetch<Season>(`/seasons/${year}`),
  create: (season: Partial<Season>) =>
    apiFetch<Season>("/seasons", {
      method: "POST",
      body: JSON.stringify(season),
    }),
};

// Drivers API
export const driversApi = {
  getAll: () => apiFetch<Driver[]>("/drivers"),
  getById: (id: string) => apiFetch<Driver>(`/drivers/${id}`),
  create: (driver: Partial<Driver>) =>
    apiFetch<Driver>("/drivers", {
      method: "POST",
      body: JSON.stringify(driver),
    }),
};

// Constructors API
export const constructorsApi = {
  getAll: () => apiFetch<Constructor[]>("/constructors"),
  getById: (id: string) => apiFetch<Constructor>(`/constructors/${id}`),
  create: (constructor: Partial<Constructor>) =>
    apiFetch<Constructor>("/constructors", {
      method: "POST",
      body: JSON.stringify(constructor),
    }),
};

// Races API
export const racesApi = {
  getAll: () => apiFetch<Race[]>("/races"),
  getById: (id: string) => apiFetch<Race>(`/races/${id}`),
  getBySeason: (year: number) => apiFetch<Race[]>(`/races/season/${year}`),
  create: (race: Partial<Race>) =>
    apiFetch<Race>("/races", {
      method: "POST",
      body: JSON.stringify(race),
    }),
};

// Telemetry API (for future use)
export const telemetryApi = {
  getLapTelemetry: (year: number, round: number, session: string, driver: string, lap: number) =>
    apiFetch<TelemetryData>(`/telemetry/${year}/${round}/${session}/telemetry/${driver}/${lap}`),
  getSessionLaps: (year: number, round: number, session: string, driver?: string) => {
    const driverParam = driver ? `?driver=${driver}` : "";
    return apiFetch<LapData[]>(`/telemetry/${year}/${round}/${session}/laps${driverParam}`);
  },
};

// Type definitions
export interface Season {
  id: string;
  year: number;
  wikipedia_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Driver {
  id: string;
  driver_id: string;
  permanent_number?: number;
  code?: string;
  given_name: string;
  family_name: string;
  date_of_birth?: string;
  nationality: string;
  url?: string;
  created_at: string;
  updated_at: string;
}

export interface Constructor {
  id: string;
  constructor_id: string;
  name: string;
  nationality: string;
  url?: string;
  created_at: string;
  updated_at: string;
}

export interface Race {
  id: string;
  season_id: string;
  round: number;
  race_name: string;
  circuit_id: string;
  circuit_name: string;
  locality: string;
  country: string;
  date: string;
  time?: string;
  url?: string;
  created_at: string;
  updated_at: string;
}

export interface TelemetryData {
  year: number;
  round: number;
  session: string;
  driver: string;
  lap: number;
  telemetry: TelemetryPoint[];
}

export interface TelemetryPoint {
  Distance: number;
  Speed: number;
  Throttle: number;
  Brake: number;
  Gear: number;
  RPM: number;
  DRS: number;
}

export interface LapData {
  LapNumber: number;
  Time: string;
  Driver: string;
  LapTime: string;
  Sector1Time: string;
  Sector2Time: string;
  Sector3Time: string;
  SpeedI1: number;
  SpeedI2: number;
  SpeedFL: number;
  SpeedST: number;
  Compound: string;
  TyreLife: number;
  IsPersonalBest: boolean;
}
