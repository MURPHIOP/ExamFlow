import { PageFrame } from "@/components/shared/page-frame";

const subjects = ["Vocal", "Tabla", "Dance", "Fine Arts", "Instrumental", "Theory"];

export default function SubjectsPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Public Catalog"
        title="Explore exam subjects"
        description="A clear public view of supported subject categories. Data will be driven by backend exam setup routes where configured."
      >
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {subjects.map((subject) => (
            <div key={subject} className="glow-card p-5 font-medium">
              {subject}
            </div>
          ))}
        </div>
      </PageFrame>
    </div>
  );
}
