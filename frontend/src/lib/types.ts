export type SeriesPoint = { t: string; v: number };

export type Metrics = {
  cagr: number;
  vol: number;
  sharpe: number;
  sortino: number;
  max_drawdown: number;
  calmar: number;
  hit_rate: number;
  turnover_mean: number;
};

export type ExperimentListItem = {
  id: number;
  name: string;
  status: string;
  created_at: string;
  sharpe?: number;
  cagr?: number;
  max_drawdown?: number;
  turnover_mean?: number;
};
