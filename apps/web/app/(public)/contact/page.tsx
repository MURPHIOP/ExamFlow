import { PageFrame } from "@/components/shared/page-frame";

export default function ContactPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Contact"
        title="Talk to M.B. Technosoft Pvt Ltd"
        description="For demos, deployment, and platform onboarding, this page gives a polished contact surface while backend contact routing is prepared."
      >
        <div className="grid gap-4 md:grid-cols-3">
          {[
            "demo@examflow.example",
            "+91 00000 00000",
            "Kolkata, India",
          ].map((item) => (
            <div key={item} className="glass-card p-5 text-sm">
              {item}
            </div>
          ))}
        </div>
      </PageFrame>
    </div>
  );
}
