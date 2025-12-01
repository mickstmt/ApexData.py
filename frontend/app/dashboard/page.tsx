export default function DashboardPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
        <p className="text-muted-foreground">
          Real-time Formula 1 telemetry and analytics
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Current Season"
          value="2024"
          icon="📅"
          change="+1"
        />
        <StatCard
          title="Total Races"
          value="24"
          icon="🏁"
          change="+2"
        />
        <StatCard
          title="Active Drivers"
          value="20"
          icon="🏎️"
          change="0"
        />
        <StatCard
          title="Constructors"
          value="10"
          icon="🏆"
          change="0"
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Races */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Races</h2>
          <div className="space-y-3">
            <RaceItem
              name="Abu Dhabi Grand Prix"
              date="Dec 8, 2024"
              status="Upcoming"
            />
            <RaceItem
              name="Qatar Grand Prix"
              date="Dec 1, 2024"
              status="Completed"
            />
            <RaceItem
              name="Las Vegas Grand Prix"
              date="Nov 24, 2024"
              status="Completed"
            />
          </div>
        </div>

        {/* Championship Leaders */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Championship Leaders</h2>
          <div className="space-y-4">
            <LeaderItem
              position={1}
              name="Max Verstappen"
              team="Red Bull Racing"
              points={575}
            />
            <LeaderItem
              position={2}
              name="Lando Norris"
              team="McLaren"
              points={473}
            />
            <LeaderItem
              position={3}
              name="Charles Leclerc"
              team="Ferrari"
              points={441}
            />
          </div>
        </div>
      </div>

      {/* Telemetry Preview */}
      <div className="bg-card border border-border rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-4">Latest Telemetry Data</h2>
        <p className="text-muted-foreground">
          Telemetry data visualization will be displayed here. Connect to a race session to see real-time data.
        </p>
      </div>
    </div>
  );
}

// Stat Card Component
function StatCard({
  title,
  value,
  icon,
  change,
}: {
  title: string;
  value: string;
  icon: string;
  change: string;
}) {
  return (
    <div className="bg-card border border-border rounded-lg p-6 hover:border-primary transition-colors">
      <div className="flex items-center justify-between mb-2">
        <span className="text-3xl">{icon}</span>
        <span className="text-sm text-muted-foreground">{change}</span>
      </div>
      <h3 className="text-sm font-medium text-muted-foreground mb-1">{title}</h3>
      <p className="text-3xl font-bold">{value}</p>
    </div>
  );
}

// Race Item Component
function RaceItem({
  name,
  date,
  status,
}: {
  name: string;
  date: string;
  status: string;
}) {
  return (
    <div className="flex items-center justify-between p-3 rounded-lg hover:bg-accent transition-colors">
      <div>
        <p className="font-medium">{name}</p>
        <p className="text-sm text-muted-foreground">{date}</p>
      </div>
      <span
        className={`px-3 py-1 rounded-full text-xs font-medium ${
          status === "Upcoming"
            ? "bg-primary/20 text-primary"
            : "bg-green-500/20 text-green-500"
        }`}
      >
        {status}
      </span>
    </div>
  );
}

// Leader Item Component
function LeaderItem({
  position,
  name,
  team,
  points,
}: {
  position: number;
  name: string;
  team: string;
  points: number;
}) {
  return (
    <div className="flex items-center gap-4 p-3 rounded-lg hover:bg-accent transition-colors">
      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
        {position}
      </div>
      <div className="flex-1">
        <p className="font-medium">{name}</p>
        <p className="text-sm text-muted-foreground">{team}</p>
      </div>
      <div className="text-right">
        <p className="font-bold">{points}</p>
        <p className="text-xs text-muted-foreground">pts</p>
      </div>
    </div>
  );
}
