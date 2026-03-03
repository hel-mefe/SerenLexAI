import AuthLayout from "@/components/layouts/AuthLayout"
import { AuthContainer } from "@/components/layouts/AuthContainer"
import { MarketingPanel } from "@/components/marketing/MarketingPanel"
import { AuthPanel } from "@/components/auth/AuthPanel"

export default function SignInPage() {
  return (
    <AuthLayout>
      <AuthContainer>
        <MarketingPanel />
        <AuthPanel />
      </AuthContainer>
    </AuthLayout>
  )
}